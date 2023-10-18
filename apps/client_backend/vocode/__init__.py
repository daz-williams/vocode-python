import os


environment = {}


def setenv(**kwargs):
    for key, value in kwargs.items():
        environment[key] = value


def getenv(key, default=None):
    return environment.get(key) or os.getenv(key, default)


api_key = ""
base_url = ""
