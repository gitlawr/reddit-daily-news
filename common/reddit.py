from typing import List, Dict

import loguru
from praw import Reddit
from praw.reddit import Submission

logger = loguru.logger


def get_submission_dict(subreddit_list: List[str], reddit: Reddit,
                        top_limit: int = 5, skip_stickied: bool = True) -> Dict[str, List[Submission]]:
    """
    获取指定subreddit的top_limit篇submission，并且以字典的形式返回，key是subreddit的名字，value是submission的列表
    :param subreddit_list:
    :param top_limit:
    :param reddit:
    :param skip_stickied: 是否跳过置顶的submission
    :return:
    """
    submission_dict = {}
    for subreddit_name in subreddit_list:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            logger.info(f"Subreddit: {subreddit_name}, ID: {subreddit.id}")
            submission_dict.setdefault(subreddit, [])
        except Exception as e:
            logger.error(f"Subreddit: {subreddit_name}, Error: {e}")
            continue

        for submission in subreddit.hot():
            if len(submission_dict[subreddit]) >= top_limit:
                break

            if skip_stickied and submission.stickied:
                continue

            submission_dict.setdefault(subreddit, []).append(submission)

    return submission_dict
