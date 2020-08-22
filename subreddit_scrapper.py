import datetime
import logging
import os
import praw
import time
from dotenv import load_dotenv

load_dotenv()
    
def get_scraped_submissions(tracked_subreddit: str):
    reddit = praw.Reddit(
            client_id=os.environ['CLIENT_ID'],
            client_secret=os.environ['CLIENT_SECRET'],
            user_agent=os.environ['USER_AGENT'],
            username=os.environ['USERNAME'],
            password=os.environ['PASSWORD']
        )

    try:
        return list(reddit.subreddit(tracked_subreddit).new(limit=10))
    except Exception as e:
        logging.info(f'{str(datetime.datetime.now())}: Failed to get scrapped submissions')
        logging.error(f'{str(datetime.datetime.now())}: {e}')
        time.sleep(10)

        return []
