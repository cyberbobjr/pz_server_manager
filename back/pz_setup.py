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
    Bootstrap.install_pzserver(app_config["pz"]["pz_exe_path"], steamcmd)
    '''
    Server not installed, so we install it, and we ask for relaunching the server, 
    that way the directory structure for server will be created
    '''
    print(f'Relaunch the server...')
    exit(0)


def get_rcon_info_if_process_running():
    if pzGame.is_process_running():
        # if PZ Server launched, we get the rcon port & rcon password from server.ini
        app_config["rcon"]["password"] = pzGame.get_server_init("RCONPassword")
        app_config["rcon"]["port"] = pzGame.get_server_init("RCONPort")


def get_discord_info():
    if "discord" in app_config and "apikey" in app_config["discord"] and "channel" in app_config["discord"]:
        try:
            pzGame.set_server_ini("DiscordToken", app_config["discord"]["apikey"])
            pzGame.set_server_ini("DiscordChannelID", app_config["discord"]["channel"])
        except FileNotFoundError:
            print(f'Ini file not found')
    else:
        app_config["discord"]["apikey"] = pzGame.pz_config.get_value("DiscordToken")
        app_config["discord"]["channel"] = pzGame.pz_config.get_value("DiscordChannelID")


steam = Steam(app_config["steam"]["apikey"], app_config["steam"]["cache_folder"], app_config["steam"]["appid"])
pzGame = PZGame(app_config["pz"]["pz_exe_path"], app_config["pz"]["server_path"], app_config["pz"]["password"])

get_rcon_info_if_process_running()
get_discord_info()

pzRcon = PZRcon(app_config["rcon"]["host"], app_config["rcon"]["port"], app_config["rcon"]["password"])
pzGame.pz_rcon = pzRcon

if app_config["discord"]["enable"] and app_config["discord"]["apikey"] and app_config["discord"]["channel"]:
    pzDiscord = PZDiscord(app_config["discord"]["apikey"], app_config["discord"]["channel"])
else:
    pzDiscord = None

pzMonitoring = app_config["pz"]["monitoring"]
