import os

import yaml

app_config = {}


def init_config(config_file):
    global app_config
    if not os.path.exists(config_file):
        print("config.yml not found !")
        exit(0)

    with open(config_file) as f:
        app_config = yaml.load(f, Loader=yaml.SafeLoader)
        if app_config['steam']['apikey'] is None:
            print("steam api key not found !")
            exit(0)
        return app_config
