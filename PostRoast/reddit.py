import json
import random
from config import YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, YOUR_USER_AGENT
import praw
import google.generativeai as genai

def load_api_key():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config['genai_api_key']

def initialize_reddit_client():
    reddit = praw.Reddit(
        client_id=YOUR_CLIENT_ID,
        client_secret=YOUR_CLIENT_SECRET,
        user_agent=YOUR_USER_AGENT
    )
    return reddit

def load_fetched_titles():
    try:
        with open('titles.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_fetched_titles(titles):
    with open('titles.json', 'w') as file:
        json.dump(titles, file, indent=4)

def fetch_and_filter():
    reddit = initialize_reddit_client()
    
    with open('subreddit.json', 'r') as file:
        subreddits = json.load(file)
    
    fetched_titles = load_fetched_titles()
    
    subreddit_name = random.choice(subreddits)

    max_word_count = 250
    min_word_count = 100
    top_limit = 50
    subreddit = reddit.subreddit(subreddit_name)
    filtered_stories = []
    count = 1
    for submission in subreddit.top(limit=top_limit,time_filter = "week"):
        if count > 3:
            break
        word_count = len(submission.selftext.split())
        if word_count <= max_word_count and submission.selftext and word_count >= min_word_count and not submission.over_18 and submission.title not in fetched_titles:
            api_key = load_api_key()
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Optimize this text for AI TTS, removing abbreviations:{submission.selftext}   Do not anything else just write Optimized text,add {submission.title} in the beginning also convert all text to upper case please.DO NOT WRITE ANYTHING ELSE JUST OPTIMIZE THE TEXT AND ADD {submission.title} IN THE BEGINNING")
            optimized_text = response.text
            submission.selftext = optimized_text
            filtered_stories.append({
                'title': submission.title,
                'selftext': submission.selftext,
                'url': submission.url
            })
            fetched_titles.append(submission.title)
            print(subreddit_name)
            print(submission.selftext) # her gönderinin değişmiş selftextini yazdırır
            count += 1
            submission.selftext.upper()


    save_fetched_titles(fetched_titles)
    
    return filtered_stories

fetch_and_filter()