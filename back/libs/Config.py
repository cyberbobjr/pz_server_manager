import yaml
import os

app_config = {}


def init_config(config_file):
    global app_config
    if not os.path.exists(config_file):
        print("config.yml not found !")
        exit(0)

    with open(config_file) as f:
        app_config = yaml.load(f, Loader=yaml.SafeLoader)
        return app_config
