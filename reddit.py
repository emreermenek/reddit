import json
import random
from config import YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, YOUR_USER_AGENT
import praw
import google.generativeai as genai


def load_api_key():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config['genai_api_key']

# Initialize the Reddit client
def initialize_reddit_client():
    reddit = praw.Reddit(
        client_id=YOUR_CLIENT_ID,
        client_secret=YOUR_CLIENT_SECRET,
        user_agent=YOUR_USER_AGENT
    )   
    return reddit

# Load previously fetched titles from JSON file
def load_fetched_titles():
    try:
        with open('titles.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save fetched titles to JSON file
def save_fetched_titles(titles):
    with open('titles.json', 'w') as file:
        json.dump(titles, file, indent=4)

# Fetch and filter top stories of all time
def fetch_and_filter():
    reddit = initialize_reddit_client()
    
    # Load subreddit names from JSON file
    with open('subreddit.json', 'r') as file:  # Updated file name
        subreddits = json.load(file)
    
    # Load previously fetched titles
    fetched_titles = load_fetched_titles()
    
    # Select a random subreddit name
    subreddit_name = random.choice(subreddits)

    max_word_count = 500  # Maximum word count for filtering
    min_word_count = 200
    top_limit = 50        # Limit on the number of "top" posts to fetch
    subreddit = reddit.subreddit(subreddit_name)
    filtered_stories = []
    count = 0
    for submission in subreddit.hot(limit=top_limit):
        if count >= 6:
            break    
        word_count = len(submission.selftext.split())
        if word_count <= max_word_count and submission.selftext and word_count >= min_word_count and not submission.over_18 and submission.title not in fetched_titles:  # Filter by word count, NSFW, and previously fetched titles
            filtered_stories.append({
                'title': submission.title,
                'selftext': submission.selftext,  # Full selftext
                'url': submission.url
            })
            fetched_titles.append(submission.title)
            api_key = load_api_key()
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(f"Optimize this text for AI TTS, removing abbreviations:{submission.selftext}  Do not anything else just write Optimized text ")
            optimized_text = response.text
            submission.selftext = optimized_text
            count += 1
    print(subreddit_name)
    print(submission.selftext)
    
    save_fetched_titles(fetched_titles)
    
    return filtered_stories

fetch_and_filter()