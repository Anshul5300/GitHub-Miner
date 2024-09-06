import requests
from flask import jsonify, session
from functools import reduce
from datetime import datetime
from backend.app.services.github_query.github_rest.client import RESTClient


def slice_dict(dictionary, keys):
    """
    Slices a dictionary to include only the specified keys.

    Args:
        dictionary (dict): The dictionary to slice.
        keys (list): A list of keys to include in the sliced dictionary.

    Returns:
        dict: A dictionary containing only the specified keys.
    """
    return {key: dictionary[key] for key in keys if key in dictionary}


def map_to_created_by(datalist):
    """
    Maps a list of dictionaries to include only the "created_at" key.
    """
    return [slice_dict(item, ["created_at"]) for item in datalist]


def paginate_list(data, pg_size, node_mapper=lambda x: x):
    """
    Paginates a list of data.

    Args:
        data (list): The list of data to paginate.
        pg_size (int): The number of items per page.
        node_mapper (function): A function to transform data["node"] to the desired format.

    Returns:
        list: A list of paginated data.
    """
    paginated_list = [data[i:i + pg_size]
                      for i in range(0, len(data), pg_size)]
    paginated_list = [{"nodes": node_mapper(page)} for page in paginated_list]
    if not paginated_list:
        paginated_list = [{"nodes": []}]
    return paginated_list


def format_response_like_graphql(data, **kwargs):
    """
    Formats a response like a GraphQL response.

    Args:
        data (dict): The data to format.
        kwargs (dict): Additional keyword arguments.

        Supported keyword arguments:
        resource (str): The resource e.g user, repo, comment, commit etc.
        resource_type (str): The type of resource e.g gist, issue, commit etc.

    Returns:
        dict: A dictionary containing the formatted response.
    """
    resource = kwargs.get("resource")
    resource_type = kwargs.get("resource_type")
    key = f'{resource_type}{resource.capitalize()}'
    res = {
        "user": {
            key: data
        },
        "pageInfo": {
            "totalCount": len(data["nodes"]),
            "hasNextPage": kwargs.get("has_next_page", False),
        },
        "login": get_current_user_login()["viewer"]["login"],
    }
    return res


def paginate_and_format_comments(comments, pg_size, resource, resource_type):
    res = []
    paginated_comments = paginate_list(comments, pg_size, map_to_created_by)
    for i, page in enumerate(paginated_comments):
        has_next_page = i < (len(paginated_comments) - 1)
        formatted_response = format_response_like_graphql(page, resource=resource,
                                                          resource_type=resource_type,
                                                          has_next_page=has_next_page)
        res.append(formatted_response)
    return res


def get_current_user_login():
    """
    Fetches the login information of the current authenticated user using the OAuth access token.

    Returns:
        dict: A dictionary containing the current user's login information, or an error message.
    """
    try:
        g = RESTClient().github
        return {"viewer": {"login": g.get_user().raw_data["login"]}}
    except Exception as e:
        return {"error": str(e)}


def get_user_gist_comments(**kwargs):
    """
    Fetches the gist comments of a specific user.

    Args:
        pg_size (int): The number of gist comments to fetch per page. Defaults to 100.

    Returns:
        dict: A dictionary containing the specified user's gist comments, or an error message.
    """
    try:
        g = RESTClient().github
        pg_size = int(kwargs.get("pg_size", 100))
        comments = []
        for gist in g.get_user().get_gists():
            if len(comments) < pg_size:
                comments.extend(
                    [comment.raw_data for comment in gist.get_comments()])
        return paginate_and_format_comments(
            comments, pg_size, "comments", "gist")
    except Exception as e:
        return {"error": str(e)}


def get_user_issue_comments(**kwargs):
    """
    Fetches the issue comments of a specific user.

    Args:
        pg_size (int): The number of issue comments to fetch per page. Defaults to 100.

    Returns:
        dict: A dictionary containing the specified user's issue comments, or an error message.
    """
    try:
        g = RESTClient().github
        pg_size = int(kwargs.get("pg_size", 100))
        comments = []
        for repo in g.get_user().get_repos():
            if len(comments) < pg_size:
                comments.extend(
                    [comment.raw_data for comment in repo.get_issues_comments()]
                )
        return paginate_and_format_comments(
            comments, pg_size, "comments", "issue")
    except Exception as e:
        return {"error": str(e)}


def get_user_commit_comments(**kwargs):
    """
    Fetches the commit comments of a specific user.

    Args:
        pg_size (int): The number of commit comments to fetch per page. Defaults to 100.

    Returns:
        dict: A dictionary containing the specified user's commit comments, or an error message.
    """
    try:
        g = RESTClient().github
        pg_size = int(kwargs.get("pg_size", 100))
        comments = []
        for repo in g.get_user().get_repos():
            if len(comments) < pg_size:
                comments.extend(
                    [comment.raw_data for comment in repo.get_comments()])
        return paginate_and_format_comments(
            comments, pg_size, "comments", "commit")
    except Exception as e:
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
    elif comment_type == "issue":
        return get_user_issue_comments(**kwargs)
    elif comment_type == "commit":
        return get_user_commit_comments(**kwargs)
    else:
        return {"error": "Invalid/Unsupported comment type"}, 400


class Http:
    """
    This is a generic class that can be used to call APIs.
    """

    BASE_URL = "https://api.github.com"

    @staticmethod
    def fetch(endpoint: str = None):
        """
        This method is used to fetch details using GitHub API. The request headers contain a auth token.

        Args:
            endpoint (str): The GitHub API endpoint to which the request has to be made

        Returns:
            A response object if the request is successfull. Throws error otherwise.
        """
        token = session.get("access_token")
        if not token:
            raise Exception({"error": "User not authenticated"})

        url = Http.BASE_URL + endpoint
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }

        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res
        else:
            raise Exception({"error": res.json()["message"]})

    @staticmethod
    def get(url=None):
        """
        This method is used to fetch details using a URL. These requests should not require any auth tokens.

        Args:
            url (str): The URL to which the request has to be made

        Returns:
            A response object if the request is successfull. Throws error otherwise.
        """
        token = session.get("access_token")
        if not token:
            raise Exception({"error": "User not authenticated"})

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }

        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res
        else:
            raise Exception({"error": res.json()["message"]})


def get_user_profile_stats(username: str):
    """
    Retrive profie details for each attributes (eg. issues) and returns the count of each attribute as a dictionary.
    It uses Http class for calling to GitHub API

    Args:
        username (str): The username whose profile stats needs to be fetched

    Returns:
        dict: A dictionary containing key statistics and information about the user, such as
            their login, creation date, company, number of followers, etc.
    """
    try:
        user = Http.fetch(f"/users/{username}").json()
        gists = Http.fetch(f"/users/{username}/gists").json()
        gist_comments = reduce(lambda acc, x: acc + x["comments"], gists, 0)
        issues = Http.fetch("/issues").json()
        print(issues)
        issue_comments = reduce(lambda acc, x: acc + x["comments"], issues, 0)
        projects = Http.fetch(f"/users/{username}/projects").json()
        repos = Http.get(user["repos_url"]).json()
        pull_requests = 0
        commit_comments = 0
        for repo in repos:
            ele = Http.fetch(f'/repos/{username}/{repo["name"]}/pulls').json()
            comments = Http.fetch(
                f'/repos/{username}/{repo["name"]}/comments').json()
            pull_requests += len(ele)
            commit_comments += len(comments)
        starred = Http.fetch(f"/users/{username}/starred").json()
        watching = Http.fetch(f"/users/{username}/subscriptions").json()

        res = {
            "commit_comments": commit_comments,
            "company": user["login"],
            "created_at": user["created_at"],
            "followers": user["followers"],
            "following": user["following"],
            "gist_comments": gist_comments,
            "gists": len(gists),
            "github": user["login"],
            "issue_comments": issue_comments,
            "issues": len(issues),
            "projects": len(projects),
            "pull_requests": pull_requests,
            "repositories": user["public_repos"],
            # "repository_discussion_comments": 0,
            # "repository_discussions": 0,
            "starred_repositories": len(starred),
            "watching": len(watching),
        }
        return jsonify(res)
    except Exception as e:
        return jsonify(e.args)


def get_user_contributions(username, start, end):
    """
    Fetch user contributions (commits, issues, repositories, pull requests, etc.) of a specific user.

    Args:
        username (str): The username of the user.

    Returns:
        dict: A dictionary containing the specified user's contributions.
    """

    def count_commits():
        for repo in repos:
            commits = Http.fetch(
                f"/repos/{username}/{repo['name']}/commits?author={user['login']}&since={start}&until={end}"
            ).json()
            if commits:
                return len(commits)
            return 0

    def count_issues():
        for repo in repos:
            issues = Http.fetch(
                f"/repos/{username}/{repo['name']}/issues?state=open&creator={username}&since={start}"
            ).json()
            if issues:
                return len(issues)
            return 0

    def count_pull_requests():
        count = 0
        for repo in repos:
            prs = Http.fetch(
                f"/repos/{username}/{repo['name']}/pulls?state=open"
            ).json()
            for pr in prs:
                start_date = datetime.strptime(
                    start.split("+")[0][1:] + "Z", r"%Y-%m-%dT%H:%M:%S%z"
                )
                end_date = datetime.strptime(
                    end.split("+")[0][1:] + "Z", r"%Y-%m-%dT%H:%M:%S%z"
                )
                created_at = datetime.strptime(
                    pr["created_at"], r"%Y-%m-%dT%H:%M:%S%z")
                if (
                    pr["head"]["user"]["login"].lower() == username.lower()
                    and created_at > start_date
                    and created_at < end_date
                ):
                    count += 1
        return count

    def count_pull_request_reviews():
        count = 0
        for repo in repos:
            prs = Http.fetch(
                f"/repos/{username}/{repo['name']}/pulls?state=closed"
            ).json()
            for pr in prs:
                start_date = datetime.strptime(
                    start.split("+")[0][1:] + "Z", r"%Y-%m-%dT%H:%M:%S%z"
                )
                end_date = datetime.strptime(
                    end.split("+")[0][1:] + "Z", r"%Y-%m-%dT%H:%M:%S%z"
                )
                closed_at = datetime.strptime(
                    pr["closed_at"], r"%Y-%m-%dT%H:%M:%S%z")
                if (
                    pr["head"]["user"]["login"].lower() == username.lower()
                    and closed_at > start_date
                    and closed_at < end_date
                ):
                    count += 1
        return count

    def count_restricted_contributions():
        repositories = Http.fetch(f"/users/{username}/repos?type=all").json()
        private_repos = list(filter(lambda x: x["private"], repositories))
        return len(private_repos)

    try:
        user = Http.fetch(f"/users/{username}").json()
        repos = Http.get(user["repos_url"]).json()
        commit_count = count_commits()
        issues = count_issues()
        pr = count_pull_requests()
        pr_reviews = count_pull_request_reviews()
        repo_contributions = len(Http.fetch(
            f"/users/{username}/repos?type=all").json())
        res_con = count_restricted_contributions()

        res = {
            "commit": commit_count,
            "issue": issues,
            "pr": pr,
            "pr_review": pr_reviews,
            "repository": repo_contributions,
            "res_con": res_con,
        }
        return jsonify(res)
    except Exception as e:
        return jsonify(e.args)


def get_user_issues(username, per_page=10):
    """
    Fetches the issues of a specific user using the OAuth access token.

    Args:
        username: The login of the user whose issues are to be fetched.
        per_page: The number of issues to fetch per page. Default is 10.
    Returns:
        dict: A dictionary containing the user's issues, or an error message.
    """
    try:
        data = Http.fetch(f"/issues?per_page={per_page}").json()
        return data
    except Exception as e:
        if 'Not Found' in str(e):
            return []
        else:
            return jsonify(e.args[0])


def get_user_gists(username, per_page=10):
    """
    Fetches the gists of a specific user using the OAuth access token.

    Args:
        username: The login of the user whose gists are to be fetched.
        per_page: The number of gists to fetch per page. Default is 10.

    Returns:
        dict: A dictionary containing the user's gists, or an error message.
    """
    try:
        data = Http.fetch(
            f"/users/{username}/gists?per_page={per_page}").json()
        return data
    except Exception as e:
        if 'Not Found' in str(e):
            return []
        else:
            return jsonify(e.args[0])


def get_user_pull_requests_by_rest(username, repo, per_page=10):
    """
    Fetches the pull requests of a specific user using the OAuth access token.

    Args:
        username: The login of the user whose pull requests are to be fetched.
        repo: The name of the repository.
        per_page: The number of pull requests to fetch per page. Default is 10.

    Returns:
        dict: A dictionary containing the user's pull requests, or an error message.
    """
    try:
        data = Http.fetch(
            f"/repos/{username}/{repo}/pulls?per_page={per_page}").json()
        return data
    except Exception as e:
        if 'Not Found' in str(e):
            return []
        else:
            return jsonify(e.args[0])


def get_user_repositories(username, per_page=10):
    """
    Fetches the repositories of a specific user using the OAuth access token.

    Args:
        username: The login of the user whose repositories are to be fetched.
        per_page: The number of repositories to fetch per page. Default is 10.

    Returns:
        dict: A dictionary containing the user's repositories, or an error message.
    """
    try:
        data = Http.fetch(
            f"/users/{username}/repos?per_page={per_page}").json()
        return data
    except Exception as e:
        if 'Not Found' in str(e):
            return []
        else:
            return jsonify(e.args[0])


def get_repository_discussions_by_rest(username, repo, pg_size=10):
    """
    Fetches the discussions of a specific repository of a user using the OAuth access token.

    Args:
        username: The login of the user whose repository discussions are to be fetched.
        repo: The name of the repository.
        per_page: The number of discussions to fetch per page. Default is 10.

    Returns:
        dict: A dictionary containing the repository's discussions, or an error message.
    """
    try:
        data = Http.fetch(
            f"/repos/{username}/{repo}/discussions?per_page={pg_size}").json()
        return data
    except Exception as e:
        if 'Not Found' in str(e):
            return []
        else:
            return jsonify(e.args[0])
