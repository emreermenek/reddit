import json
import random
from config import YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, YOUR_USER_AGENT
import praw

# Initialize the Reddit client
def initialize_reddit_client():
    reddit = praw.Reddit(
        client_id=YOUR_CLIENT_ID,
        client_secret=YOUR_CLIENT_SECRET,
        user_agent=YOUR_USER_AGENT
    )   
    return reddit

# Fetch and filter hot stories
def fetch_and_filter():
    reddit = initialize_reddit_client()
    
    # Load subreddit names from JSON file
    with open('subreddits.json', 'r') as file:
        subreddits = json.load(file)
    
    # Select a random subreddit name
    subreddit_name = random.choice(subreddits)
    subreddits.remove(subreddit_name)

    with open('subreddits.json', 'w') as file:
        json.dump(subreddits, file, indent=4)

    max_word_count = 400  # Maximum word count for filtering
    min_word_count = 100
    hot_limit = 100        # Limit on the number of "hot" posts to fetch
    subreddit = reddit.subreddit(subreddit_name)
    filtered_stories = []
    for submission in subreddit.hot(limit=hot_limit):
        word_count = len(submission.selftext.split())
        if word_count <= max_word_count and submission.selftext and word_count >= min_word_count:  # Filter by word count
            filtered_stories.append({
                'title': submission.title,
                'selftext': submission.selftext,  # Full selftext
                'url': submission.url
            })
    print(subreddit_name)
    print(filtered_stories)
    return filtered_stories

fetch_and_filter()
