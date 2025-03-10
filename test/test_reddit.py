import os
from typing import List

import dotenv
import loguru
import praw
import pytest
from praw import Reddit

from common.reddit import get_submission_dict

logger = loguru.logger
dotenv.load_dotenv()


@pytest.fixture
def subreddit_list():
    """
    获取subreddit列表
    :return:
    """
    subreddit_list_str = os.getenv("SUBREDDIT_LIST")
    return subreddit_list_str.split(",")


@pytest.fixture
def reddit():
    """
    获取reddit实例
    :return:
    """
    return praw.Reddit("bot1", user_agent="bot1 user agent")


def test_get_submission_dict(subreddit_list: List[str], reddit: Reddit):
    top_limit = int(os.getenv("TOP_LIMIT", 5))
    submission_dict = get_submission_dict(subreddit_list, reddit, top_limit)

    assert len(submission_dict) == len(subreddit_list)

    for subreddit_name, submission_list in submission_dict.items():
        for submission in submission_list:
            title_info = f"Subreddit: {subreddit_name}, Score: {submission.score}, Title: {submission.title}"
            logger.info(title_info)


def test_generate_reddit_daily_markdown(subreddit_list: List[str], reddit: Reddit):
    submission_dict = get_submission_dict(subreddit_list, reddit)
    from common.reddit import generate_reddit_daily_markdown
    markdown_content = generate_reddit_daily_markdown(submission_dict)
    logger.info(markdown_content)
