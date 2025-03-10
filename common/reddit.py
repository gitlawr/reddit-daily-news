import datetime
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


def generate_reddit_daily_markdown(subreddit_data: Dict[str, List[Submission]]):
    """
    生成Reddit每日新闻的Markdown内容
    :param subreddit_data:
    :return:
    """
    # 获取当前日期并格式化为YYYY-MM-DD
    current_date = datetime.date.today().strftime("%Y-%m-%d")

    # 初始化Markdown内容，添加主标题
    markdown_content = [f"# Reddit News Daily {current_date}"]

    # 遍历每个subreddit（按字母顺序排序）
    for subreddit in subreddit_data.keys():
        # 添加子标题
        markdown_content.append(f"\n## {subreddit}")

        # 添加该subreddit下的所有帖子链接
        for submission in subreddit_data[subreddit]:
            title, link, score = submission.title, submission.url, submission.score
            comment_length = len(submission.comments)
            markdown_content.append(f"- [{title}]({link})")
            markdown_content.append(f"  - Score: {score}, Comments: {comment_length}")

    # 将列表合并为字符串并返回
    return '\n'.join(markdown_content)
