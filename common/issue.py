from typing import Optional

import loguru
from github import Auth, Github
from github.Issue import Issue

logger = loguru.logger


def get_github_instance(github_token: str):
    """
    获取github的实例
    :param github_token:
    :return:
    """
    auth = Auth.Token(github_token)

    return Github(auth=auth)


def open_issue(github: Github, repo_name: str, title: str, body: str) -> Optional[Issue]:
    """
    创建issue
    :param github:
    :param repo_name:
    :param title:
    :param body:
    :return:
    """
    try:
        repo = github.get_repo(repo_name)
        logger.info(f"Repo: {repo.name}, ID: {repo.id}")
    except Exception as e:
        logger.error(f"Repo: {repo_name}, Error: {e}")
        return None

    issue = repo.create_issue(title=title, body=body)
    return issue
