import os

from libs.Bootstrap import Bootstrap
from libs.Config import init_config
from libs.PZDiscord import PZDiscord
from libs.PZGame import PZGame
from libs.PZRcon import PZRcon
from libs.Steam import Steam
from libs.Steamcmd import Steamcmd, SteamcmdException

CONF_FILE = "config.yml"
app_config = init_config(CONF_FILE)
steamcmd_path = os.path.join(app_config["steam"]["steamcmd_path"])
pz_exe_path = app_config["pz"]["pz_exe_path"]

# check dirs
if not os.path.isdir(steamcmd_path):
    os.mkdir(steamcmd_path)
steamcmd = Steamcmd(steamcmd_path)
try:
    install_result = steamcmd.install()
    if install_result is not None:
        print(install_result)
        exit(0)
except SteamcmdException as e:
    print(e)

if not Bootstrap.is_pzserver_installed(app_config["pz"]["pz_exe_path"]):
    print(f'Installing PZ Dedicated Server to {pz_exe_path}')
    steamcmd.install_gamefiles(380870, pz_exe_path)
    '''
    Server not installed, so we install it, and we ask for relaunching the server, 
    that way the directory structure for server will be created
    '''
    print(f'Relaunch the server...')
    exit(0)

steam = Steam(app_config["steam"]["apikey"], app_config["steam"]["cache_folder"], app_config["steam"]["appid"])
pzGame = PZGame(app_config["pz"]["pz_exe_path"], app_config["pz"]["server_path"], app_config["pz"]["password"],
                app_config["pz"]["server_name"], app_config["pz"]["monitoring"])

pzRcon = PZRcon(app_config["rcon"]["host"], app_config["rcon"]["port"], app_config["rcon"]["password"])
pzGame.pz_rcon = pzRcon

pzDiscord = None
if "discord" in app_config and app_config["discord"].get("enable") is True:
    # Assuming PZDiscord initialization requires an apikey and a channel ID
    pzDiscord = PZDiscord(app_config["discord"]["apikey"], app_config["discord"]["channel"])

pzMonitoring = app_config["pz"]["monitoring"]
