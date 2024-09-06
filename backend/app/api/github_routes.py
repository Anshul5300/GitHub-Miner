from datetime import datetime
from flask import Blueprint, jsonify, request
from typing import List, Dict

from backend.app.services.github_graphql_services import (
    get_user_repository_discussions,
    get_user_pull_requests,
    get_user_repositories,
    get_current_user_login
)
from backend.app.services.github_rest_services import (
    get_repository_discussions_by_rest,
    get_user_pull_requests_by_rest,
)
import backend.app.services.github_graphql_services as graphql_services
import backend.app.services.github_rest_services as rest_services

github_bp = Blueprint("api", __name__)


@github_bp.route("/<api_type>/current-user-login", methods=["GET"])
def current_user_login(api_type):
    service = get_service_by_api_type(api_type)
    return service.get_current_user_login()


@github_bp.route("/graphql/user-login/<username>", methods=["GET"])
def specific_user_login(username):
    return graphql_services.get_specific_user_login(username)


@github_bp.route("/<api_type>/user-<comment_type>-comments", methods=["GET"])
def user_comments_by_type(api_type, comment_type):
    service = get_service_by_api_type(api_type)
    return service.get_user_comments_by_type(comment_type, **request.args)


@github_bp.route("/<api_type>/user-stats/<username>", methods=["GET"])
def user_stats(api_type, username):
    service = get_service_by_api_type(api_type)
    return service.get_user_profile_stats(username)



@github_bp.route("/<api_type>/user-contributions/<username>/<start>/<end>", methods=["GET"])
def user_contributions(api_type, username, start, end):
    service = get_service_by_api_type(api_type)
    start = str(datetime.strptime(start, r"%Y-%m-%dT%H:%M"))
    start = '"' + "T".join(start.split()) + '"'
    end = str(datetime.strptime(end, r"%Y-%m-%dT%H:%M"))
    end = '"' + "T".join(end.split()) + '"'
    return service.get_user_contributions(username, start, end)


@github_bp.route("/<api_type>/user-gists/<username>", methods=["GET"])
def user_gists(api_type, username):
    service = get_service_by_api_type(api_type)
    pg_size = 10
    return service.get_user_gists(username, pg_size)


@github_bp.route("/<api_type>/user-issues/<username>", methods=["GET"])
def user_issues(api_type, username):
    service = get_service_by_api_type(api_type)
    pg_size = 10
    return service.get_user_issues(username, pg_size)


@github_bp.route("/graphql/user-repository-discussions/<username>", methods=["GET"])
def user_repository_discussions(username):
    pg_size = 10
    data = get_user_repository_discussions(username, pg_size)
    return jsonify(data)


# @github_bp.route("/<api_type>/user-repositories/<username>", methods=["GET"])
# def user_repositories(api_type, username):
#    service = get_service_by_api_type(api_type)
#    pg_size = 10
#    return service.get_user_repositories(username, pg_size)

@github_bp.route('/graphql/user-repositories/<username>', methods=['GET'])
def user_repositories(username):
   pg_size = 10
   is_fork: bool = False 
   ownership = "OWNER"
   order_by = {"field": "CREATED_AT", "direction": "DESC"}
   data = get_user_repositories(username, pg_size, is_fork, ownership,order_by)
   return data,200
   
   

@github_bp.route('/graphql/userss/<username>', methods=['GET'])
def user_timepass(username):
    return {}

@github_bp.route("/graphql/user-pull-requests/<username>", methods=["GET"])
def user_pull_requests(username):
    pg_size = 10
    data = get_user_pull_requests(username, pg_size)
    return jsonify(data)


@github_bp.route("/rest/user-pull-requests/<username>/<repo>", methods=["GET"])
def user_pull_requests_by_rest(username, repo):
    per_page = 10
    data = get_user_pull_requests_by_rest(username, repo, per_page)
    return jsonify(data)


@github_bp.route("/rest/repository-discussions/<username>/<repo>", methods=["GET"])
def repository_discussions_by_rest(username, repo):
    pg_size = 10
    data = get_repository_discussions_by_rest(username, repo, pg_size)
    return jsonify(data)


def get_service_by_api_type(api_type):
    if api_type == "graphql":
        return graphql_services
    else:
        return rest_services
