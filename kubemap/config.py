import os

config = None


class Config:
    def __init__(self):
        self.server = os.getenv('SERVER')
        self.token = os.getenv('TOKEN')


def get_config():
    global config
    if config is None:
        config = Config()
    return config
