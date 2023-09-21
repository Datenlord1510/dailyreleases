import logging
import re
import praw
from praw.models import Submission
from .Config import CONFIG

logger = logging.getLogger(__name__)


praw = praw.Reddit(**CONFIG.CONFIG["reddit"])


def send_pm(recipient, title, text) -> None:
    logger.info("Sending PM to u/%s", recipient)
    return praw.redditor(recipient).message(title, text)


def submit_post(title, text, subreddit) -> Submission:
    logger.info("Submitting post to r/%s", subreddit)
    return praw.subreddit(subreddit).submit(title, text)


def get_previous_daily_post(subreddit) -> Submission:
    logger.info("Getting previous daily post from r/%s", subreddit)
    posts = praw.subreddit(subreddit).search(
        'title:"daily releases"', sort="new", syntax="lucene",
        time_filter="week")
    return next(p for p in posts if re.search(
        "daily release.*[(].* \d\d\d\d[)]", p.title, flags=re.IGNORECASE))

class RedditHandler:
    def __init__(self):
        self.praw = praw.Reddit(**CONFIG.CONFIG["reddit"])

    def submit_post(self, title: str, text: str, subreddit: str) -> Submission:
        logger.info("Submitting post to r/%s", subreddit)
        return self.praw.subreddit(subreddit).submit(title, text)

    def get_previous_daily_post(self, subreddit: str) -> Submission:
        logger.info("Getting previous daily post from r/%s", subreddit)
        posts = self.praw.subreddit(subreddit).search(
            'title:"daily releases"', sort="new", syntax="lucene",
            time_filter="week")
        return next(p for p in posts if re.search(
            "daily release.*[(].* \d\d\d\d[)]", p.title, flags=re.IGNORECASE))