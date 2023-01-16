from back import init_app
from back.libs.Config import init_config, app_config

CONF_FILE = "config.yml"

if __name__ == "__main__":
    app_config = init_config(CONF_FILE)
    app = init_app()
    app.run("127.0.0.1", port=app_config['server']['port'])
