import praw
from praw.exceptions import APIException
import sys
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

REDDIT_USERNAME = "DutchFIREBot"
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")


def main():
    reddit = praw.Reddit(user_agent='DutchFIREBot v1.0',
                         client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET,
                         username=REDDIT_USERNAME, password=REDDIT_PASSWORD)
    subreddit = reddit.subreddit('DutchFIRE')

    # create sorted array of weekdraadjes
    weekdraadjes = []
    for s in subreddit.search("Weekdraadje", time_filter='month'):
        if "weekdraadje" in s.title.lower():
            weekdraadjes.append(s)

    weekdraadjes.sort(key=lambda x: x.created_utc, reverse=True)

    # go through weekdraadjes, build chain
    for prev, s in zip(weekdraadjes[1:], weekdraadjes):
        if not has_chain_comment(s) and prev:
            try:
                s.reply("Vorige weekdraadje: [%s](%s)" % (prev.title, prev.permalink))
                sys.exit()
            except APIException:
                # we're probably rate limited. exit script.
                sys.exit("Bot is rate limited")


def has_chain_comment(submission):
    """
    Returns true if the given thread already contains a chain comment by DutchFireBOT

    :param submission:
    :return: boolean
    """

    for comment in submission.comments:
        if comment.author is not None and comment.author.name == REDDIT_USERNAME:
            return True

    return False


if __name__ == "__main__":
    main()