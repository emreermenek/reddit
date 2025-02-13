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
    reddit = initialize_reddit_client();
    # Settings
    #subreddit_name = "TrueHorrorStories" # guzel reddit 2. gün aynı hikayeleri buldu
    #subreddit_name = "scarystories" # 1 tane buldu
    subreddit_name = "creepypasta"
    #subreddit_name = 'shortscarystories'
    #subreddit_name = "nosleep" # kısa hikaye bulunmuyor
    max_word_count = 400  # Maximum word count for filtering
    min_word_count = 100
    hot_limit = 150        # Limit on the number of "hot" posts to fetch
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
    return filtered_stories;


