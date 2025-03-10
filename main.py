import argparse
import datetime

import dotenv
import loguru
import praw
from github.Issue import Issue

from common.issue import get_github_instance, open_issue
from common.reddit import get_submission_dict, generate_reddit_daily_markdown

logger = loguru.logger
dotenv.load_dotenv()


def main(praw_client_id: str, praw_client_secret: str, subreddit_list_str: str, github_token: str,
         github_repo: str = "xunjieliu/reddit-daily-news", top_limit: int = 10):
    """
    根据输入的参数，获取Reddit的每日新闻，并且生成Markdown内容，然后创建一个Github Issue
    :param praw_client_id:
    :param praw_client_secret:
    :param subreddit_list_str:
    :param github_repo:
    :param github_token:
    :param top_limit:
    :return:
    """
    subreddit_list = subreddit_list_str.split(",")
    reddit = praw.Reddit(client_id=praw_client_id, client_secret=praw_client_secret, user_agent="bot1 user agent")

    submission_dict = get_submission_dict(subreddit_list, reddit, top_limit=top_limit)
    markdown_content = generate_reddit_daily_markdown(submission_dict)

    github = get_github_instance(github_token)
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    issue: Issue = open_issue(github, github_repo, f"Reddit News Daily {current_date}", markdown_content)
    issue.lock("resolved")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--praw-client-id", required=True, help="PRAW Client ID")
    parser.add_argument("--praw-client-secret", required=True, help="PRAW Client Secret")
    parser.add_argument("--subreddit-list", required=True, help="Subreddit List")
    parser.add_argument("--github-repo", required=False, help="Github Repo", default="xunjieliu/reddit-daily-news")
    parser.add_argument("--github-token", required=True, help="Github Token")
    parser.add_argument("--top-limit", required=False, help="Top Limit", default=10, type=int)

    args = parser.parse_args()

    main(args.praw_client_id, args.praw_client_secret, args.subreddit_list,
         args.github_token, args.github_repo,
         args.top_limit)
