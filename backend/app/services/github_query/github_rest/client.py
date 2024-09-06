from github import Github, Auth
from flask import session


class RESTClient:
    """
    A singleton class that creates a single instance of the PyGithub REST API client.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.github = Github(auth=Auth.Token(session.get("access_token")))
