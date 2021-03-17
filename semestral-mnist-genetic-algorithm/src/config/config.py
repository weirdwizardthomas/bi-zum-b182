import json

CONFIG_FILE = '../src/config/config.json'


class Config:
    instance = None

    class __Config:
        def __init__(self):
            with open(CONFIG_FILE, 'r') as config_file:
                self.data = json.load(config_file)

    def __init__(self):
        if Config.instance is None:
            Config.instance = Config.__Config()

    def __getattr__(self, item):
        return getattr(self.instance, item)
