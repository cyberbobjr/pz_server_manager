from mcrcon import MCRcon
from libs.PZGame import PZGame
from flask import Flask
from yaml import SafeLoader
import yaml

WKSPATH = "/Users/benjaminmarchand/IdeaProjects/project-zomboid-server-docker/workshop-mods/content/108600"
CONF_FILE = "config.yml"

# pz_game = PZGame(WKSPATH)

app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return {
#         "result": "ok"

#     }


# with MCRcon('127.0.0.1', port=27015, password='TheBestPassword') as client:
#     print(client.command('quit'))
# pz_game = PZGame(WKSPATH)
# pz_game.display_mods_infos()
# pz_game.buildServerTestFile()
# pz_game.exportAllMods()
with open(CONF_FILE) as f:
    data = yaml.load(f, Loader=SafeLoader)
    WKSPATH = data['pz']['path'];