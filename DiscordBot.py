import discord
import os
from discord.ext import commands
from pymongo import MongoClient

MongoDBString = os.getenv('MONGODB_STRING')
botID = os.getenv('DISCORD_BOT_ID')

client = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@client.event
async def on_ready(): #event runs on startup
    print('Bot ready')

    cluster, collections = connectMongoDB()
    #loops through the guilds the bot is in and verfies the information in the database
    for guild in client.guilds:
        guildFound = collections.find_one({"guildID":guild.id})
        if not guildFound:
            info = {
                'guildID':guild.id,
                'search':{},
                'postIDs':[]
                    }
            collections.insert(info)

    cluster.close()
    client.get_cog('GetRedditPosts').searchPosts.start() #start web scraping

@client.event
async def on_guild_join(guild):
        cluster, collections = connectMongoDB()
        #add guild info to database when bot is added to a new guild
        try:
            channel = client.get_channel(guild.text_channels[0].id) #defaults to the first text channel

            info = {
            'guildID':guild.id,
            'search':{},
            'postIDs':[]
                }
            collections.insert(info)

            await channel.send('Thanks for using Reddit Post Alert Bot\nType !help for a list of commands')   
        except IndexError:
            to_leave = client.get_guild(guild.id)
            await to_leave.leave()
        
        cluster.close()

@client.event
async def on_guild_remove(guild):
    cluster, collections = connectMongoDB()
    collections.delete_many({'guildID':guild.id}) #remove guild info from database

    cluster.close()

@client.event
async def on_guild_channel_delete(channel):
    cluster, collections = connectMongoDB()
    guildFound = collections.find_one({"guildID":channel.guild.id})
    affectedSubs = ""
    for sub in guildFound['search'].items():
        if sub[1]['textChannel'] == channel.id:
            affectedSubs += (f"r/{sub[0]}, ")

    try:
        channel1 = client.get_channel(channel.guild.text_channels[0].id)
        await channel1.send(f"Text channel feeds for {affectedSubs.rstrip(' ,')} has been deleted. Please update with new text channel or remove them from search")
    except IndexError:
        owner = client.get_user(channel.guild.owner_id)
        await owner.send(f"I have left your guild [{channel.guild.name}] due no text channels. Invite me again if you still need my services.")

        await on_guild_remove(channel.guild)
        to_leave = client.get_guild(channel.guild.id)
        await to_leave.leave()
        
    cluster.close()

#Retrive the cluster and collection holding guild data to be used
def connectMongoDB():
    cluster = MongoClient(MongoDBString)
    collections = cluster['discordbot']['guildsData']
    return cluster, collections

#loads files in the cogs folder
for file in os.listdir('cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

client.run(botID)