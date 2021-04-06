import praw
import os
import time

def logIn():
    username = os.getenv('REDDIT_BOT_USERNAME')
    password = os.getenv('REDDIT_BOT_PASSWORD')
    client_id = os.getenv('REDDIT_BOT_ID')
    client_secret = os.getenv('REDDIT_BOT_SECRET')
    user_agent = os.getenv('REDDIT_BOT_AGENT')
    return  praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, username=username, user_agent=user_agent)

def ScrapePosts(sub, keywords):
    reddit = logIn()
    subreddit = reddit.subreddit(sub)

    print("reddit script running")
    posts = []

    #gets the last 35 posts from a subreddit and checks title for matching search keywords
    for submission in subreddit.new(limit = 35):
        if keywords == {'Everything*':None}:
            posts.append(submission)
        else:
            title = cleanTitle(submission.title).split()
            flair = cleanTitle(submission.link_flair_text) if submission.link_flair_text else None
            for keyword in keywords:
                if len(keyword) == 1:
                    if any([keyword == word for word in title]):
                        posts.append(submission)
                        break
                elif any([word.startswith(keyword) and len(keyword) >= len(word.rstrip("'es?:!.")) for word in title]):
                    posts.append(submission)
                    break
                elif keyword == flair:
                        posts.append(submission)
                        break
    time.sleep(1)    

    return posts

#return the proper name of a subreddit with capitilization
def getSubredditName(sub):
    reddit = logIn()
    try: 
        subreddit = reddit.subreddit(sub)
        subreddit.id
        return subreddit.display_name
    except Exception:
        return None
       
def cleanTitle(text):
    for c in "\"[]{}()*_,~":
        if c in text:
            text = text.replace(c," ")
    return text.lower().strip()