from datetime import date, datetime
from flask import session, jsonify
from typing import List, Dict

# Import client, exceptions, and authentication classes
from backend.app.services.github_query.github_graphql.client import (
    Client,
    QueryFailedException,
)
from backend.app.services.github_query.github_graphql.authentication import (
    PersonalAccessTokenAuthenticator,
)

from backend.app.services.github_query.queries.profiles.user_login import (
    UserLoginViewer,
    UserLogin,
)
from backend.app.services.github_query.queries.comments.user_gist_comments import (
    UserGistComments,
)
from backend.app.services.github_query.queries.comments.user_repository_discussion_comments import (
    UserRepositoryDiscussionComments,
)
from backend.app.services.github_query.queries.comments.user_issue_comments import (
    UserIssueComments,
)
from backend.app.services.github_query.queries.comments.user_commit_comments import (
    UserCommitComments,
)
from backend.app.services.github_query.queries.profiles.user_profile_stats import (
    UserProfileStats,
)
from backend.app.services.github_query.queries.time_range_contributions.user_contributions_collection import (
    UserContributionsCollection,
)
from backend.app.services.github_query.queries.contributions.user_gists import UserGists
from backend.app.services.github_query.queries.contributions.user_issues import (
    UserIssues,
)
from backend.app.services.github_query.queries.contributions.user_repositories import (
    UserRepositories,
)
from backend.app.services.github_query.queries.contributions.user_pull_requests import (
    UserPullRequests,
)
from backend.app.services.github_query.queries.contributions.user_repository_discussions import (
    UserRepositoryDiscussions,
)


def get_current_user_login():
    """
    Fetches the login information of the current authenticated user using the OAuth access token.

    Returns:
        dict: A dictionary containing the current user's login information, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}

    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserLoginViewer()
        response = client.execute(query=query, substitutions={})
        return response
    except QueryFailedException as e:
        return {"error": str(e)}


def get_specific_user_login(username: str):
    """
    Fetches the login and profile information of a specific user.

    Args:
        username (str): The username of the user.

    Returns:
        dict: A dictionary containing the specified user's login and profile information.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserLogin()
        response = client.execute(query, substitutions={"user": username})
        return response
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_gist_comments(**kwargs):
    """
    Fetches the gist comments of a specific user.

    Args:
        pg_size (int): The number of gist comments to fetch per page. Defaults to 100.

    Returns:
        dict: A dictionary containing the specified user's gist comments, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserGistComments()
        user = get_current_user_login()
        if "error" in user:
            raise QueryFailedException("User not authenticated")
        else:
            username = user["viewer"]["login"]
            response = client.execute(
                query,
                substitutions={"user": username,
                               "pg_size": kwargs.get("pg_size", 100)},
            )
            return list(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_repository_discussion_comments(**kwargs):
    """
    Fetches the repository discussion comments of a specific user.

    Args:
        pg_size (int): The number of repository discussion comments to fetch per page. Defaults to 100.

    Returns:
        dict: A dictionary containing the specified user's repository discussion comments, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserRepositoryDiscussionComments()
        user = get_current_user_login()
        if "error" in user:
            raise QueryFailedException("User not authenticated")
        else:
            username = user["viewer"]["login"]
            response = client.execute(
                query,
                substitutions={"user": username,
                               "pg_size": kwargs.get("pg_size", 100)},
            )
            return list(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_issue_comments(**kwargs):
    """
    Fetches the issue comments of a specific user.

    Args:
        pg_size (int): The number of issue comments to fetch per page. Defaults to 100.

    Returns:
        dict: A dictionary containing the specified user's issue comments, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserIssueComments()
        user = get_current_user_login()
        if "error" in user:
            raise QueryFailedException("User not authenticated")
        else:
            username = user["viewer"]["login"]
            response = client.execute(
                query,
                substitutions={"user": username,
                               "pg_size": kwargs.get("pg_size", 100)},
            )
            return list(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_commit_comments(**kwargs):
    """
    Fetches the commit comments of a specific user.

    Args:
        pg_size (int): The number of commit comments to fetch per page. Defaults to 100.

    Returns:
        dict: A dictionary containing the specified user's commit comments, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserCommitComments()
        user = get_current_user_login()
        if "error" in user:
            raise QueryFailedException("User not authenticated")
        else:
            username = user["viewer"]["login"]
            response = client.execute(
                query,
                substitutions={"user": username,
                               "pg_size": kwargs.get("pg_size", 100)},
            )
            return list(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_comments_by_type(comment_type, **kwargs):
    """
    Fetches the comments of a specific type of a specific user.

    Args:
        comment_type (str): The type of comments to fetch.
        pg_size (int): The number of comments to fetch per page. Defaults to 100.

    Returns:
        dict: A dictionary containing the specified user's comments of the specified type, or an error message.
    """
    if comment_type == "gist":
        return get_user_gist_comments(**kwargs)
    elif comment_type == "repository-discussion":
        return get_user_repository_discussion_comments(**kwargs)
    elif comment_type == "issue":
        return get_user_issue_comments(**kwargs)
    elif comment_type == "commit":
        return get_user_commit_comments(**kwargs)
    else:
        return {"error": "Invalid comment type"}


def get_user_profile_stats(username: str):
    """
    Fetches the profile statistics of a specific user.

    Args:
        username (str): The username of the user.

    Returns:
        dict: A dictionary containing the specified user's profile statistics.
    """
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserProfileStats()
        response = client.execute(query, substitutions={"user": username})
        return UserProfileStats.profile_stats(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_contributions(username: str, start: str, end: str):
    """
    Fetches the user contributions (commits, issues, repositories, pull requests, etc.) of a specific user.

    Args:
        username (str): The username of the user.

    Returns:
        dict: A dictionary containing the specified user's contributions.
    """
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserContributionsCollection()
        response = client.execute(
            query=query, substitutions={
                "user": username, "start": start, "end": end}
        )
        return UserContributionsCollection.user_contributions_collection(response)
    except QueryFailedException as e:
        return {"error": str(e)}
        return {"error": str(e)}


def get_user_gists(username: str, pg_size: int = 10):
    """
    Fetches the gists of a specific user using the OAuth access token.

    Args:
        user: The login of the user whose gists are to be fetched.
        pg_size: The number of gists to fetch per page. Default is 10.

    Returns:
        dict: A dictionary containing the user's gists, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}

    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserGists()
        response_generator = client.execute(
            query=query, substitutions={"user": username, "pg_size": pg_size}
        )
        response = next(response_generator, None)
        if response is None:
            return {"error": "No response received"}
        return UserGists.user_gists(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_issues(username: str, pg_size: int = 10):
    """
    Fetches the issues of a specific user using the OAuth access token.

    Args:
        user: The login of the user whose issues are to be fetched.
        pg_size: The number of issues to fetch per page. Default is 10.

    Returns:
        dict: A dictionary containing the user's issues, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}

    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserIssues()
        response_generator = client.execute(
            query=query, substitutions={"user": username, "pg_size": pg_size}
        )
        response = next(response_generator, None)
        if response is None:
            return {"error": "No response received"}
        return UserIssues.user_issues(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_repositories(username: str, pg_size: int = 10, is_fork: bool = False, ownership: str = "OWNER", order_by: Dict[str, str] = {"field": "CREATED_AT", "direction": "DESC"}):
    """
    Fetches the repositories of a specific user using the OAuth access token.

    Args:
        user: The login of the user whose repositories are to be fetched.
        pg_size: The number of repositories to fetch per page. Default is 10.

    Returns:
        dict: A dictionary containing the user's repositories, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}

    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )
    ownership_str = str(ownership).replace("'", '"')
    try:
        query = UserRepositories()
        response_generator = client.execute(
            query=query, substitutions={"user": username, "pg_size": pg_size, "is_fork": is_fork,  # replace with the actual value
        "ownership": ownership_str,  # replace with the actual value
        "order_by": order_by}
        )
        response = next(response_generator, None)
        if response is None:
            return {"error": "No response received"}
        return response
    except QueryFailedException as e:
        return {"error": str(e)}
        


def get_user_pull_requests(username: str, pg_size: int = 10):
    """
    Fetches the pull requests of a specific user using the OAuth access token.

    Args:
        user: The login of the user whose pull requests are to be fetched.
        pg_size: The number of pull requests to fetch per page. Default is 10.

    Returns:
        dict: A dictionary containing the user's pull requests, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}

    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserPullRequests()
        response_generator = client.execute(
            query=query, substitutions={"user": username, "pg_size": pg_size}
        )
        response = next(response_generator, None)
        if response is None:
            return {"error": "No response received"}
        return UserIssues.user_issues(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_repository_discussions(username: str, pg_size: int = 10):
    """
    Fetches the repository discussions of a specific user using the OAuth access token.

    Args:
        user: The login of the user whose repository discussions are to be fetched.
        pg_size: The number of repository discussions to fetch per page. Default is 10.

    Returns:
        dict: A dictionary containing the user's repository discussions, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}

    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserRepositoryDiscussions()
        response_generator = client.execute(
            query=query, substitutions={"user": username, "pg_size": pg_size}
        )
        response = next(response_generator, None)
        if response is None:
            return {"error": "No response received"}
        return UserIssues.user_issues(response)
    except QueryFailedException as e:
        return {"error": str(e)}
