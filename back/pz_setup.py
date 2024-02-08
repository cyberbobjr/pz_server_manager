import os

from libs.Config import init_config
from libs.PZDiscord import PZDiscord
from libs.PZGame import PZGame
from libs.PZRcon import PZRcon
from libs.Steam import Steam
from libs.Steamcmd import Steamcmd, SteamcmdException

CONF_FILE = "config.yml"
app_config = init_config(CONF_FILE)
steamcmd_path = os.path.join(app_config["steam"]["steamcmd_path"])


def set_rcon_info():
    if pzGame.is_process_running():
        # if PZ Server launched, we get the rcon port & rcon password from server.ini
        return [pzGame.get_server_init("RCONPassword"), pzGame.get_server_init("RCONPort")]
        # if PZ Server not launched, we set the rcon port & rcon password from config.yml
    return [app_config["rcon"]["password"], app_config["rcon"]["port"]]


# check dirs
if not os.path.isdir(steamcmd_path):
    os.mkdir(steamcmd_path)
steamcmd = Steamcmd(steamcmd_path)
try:
    steamcmd.install()
except SteamcmdException as e:
    print(e)

steam = Steam(app_config["steam"]["apikey"], app_config["steam"]["cache_folder"], app_config["steam"]["appid"])
pzGame = PZGame(app_config["pz"]["pz_exe_path"], app_config["pz"]["server_path"], app_config["pz"]["password"])

[app_config["rcon"]["password"], app_config["rcon"]["port"]] = set_rcon_info()
pzRcon = PZRcon(app_config["rcon"]["host"], app_config["rcon"]["port"], app_config["rcon"]["password"])
pzGame.pz_rcon = pzRcon

if app_config["discord"]["apikey"] and app_config["discord"]["channel"]:
    pzDiscord = PZDiscord(app_config["discord"]["apikey"], app_config["discord"]["channel"])
else:
    pzDiscord = None
