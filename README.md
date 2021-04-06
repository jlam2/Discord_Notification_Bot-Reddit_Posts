# Discord-Reddit-Notification-Bot

Discord bot that sends reddit post links to your Discord server when a new post matches your keywords critiera.

## Usage
```
!addSubreddit <Subreddit Name> <Server Text channel name> Optional*<keywords to search for>
!removeSubreddit <Subreddit name>
!addKeywords <Subreddit name> <keyterms to add>
!removeKeywords <Subreddit name(case sensitive)> <keyterms to remove>
!changeChannelFeed <Subreddit name> <Server Text channel name>

#NOTE - characters "[]{}()*_,~ will be omitited from keywords
```
To get notifications of all new posts from a specific subreddit
```
!searchAllNew <Subreddit name>
#NOTE - will overide any keywords if used on an existing subbreddit that was being monitered
```

To see which subreddits are being monitored and thier respective search keywords
```
!listSearch
```

