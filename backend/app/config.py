import os


class Config(object):
    DEBUG = True  # Ensure debug is enabled in your configuration for development
    # Consider using environment variables
    SECRET_KEY = os.environ.get("SECRET_KEY")


class AuthConfig(Config):
    GITHUB_OAUTH_CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
    GITHUB_OAUTH_CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")


class DBConfig(Config):
    MYSQL_DATABASE_USER = "tester"
    MYSQL_DATABASE_PASSWORD = os.environ.get("MYSQL_DATABASE_PASSWORD")
    MYSQL_DATABASE_DB = "github_graphql"
    MYSQL_DATABASE_HOST = "localhost"  # or your MySQL server address
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_DATABASE_USER}:{MYSQL_DATABASE_PASSWORD}@{MYSQL_DATABASE_HOST}/{MYSQL_DATABASE_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
