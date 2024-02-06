import os

from libs import Config
from libs.PZGame import PZGame
from libs.Rcon import PZRcon
from libs.SteamcmdException import Steamcmd


class Bootstrap:
    def __init__(self, app_config: Config, steamcmd: Steamcmd, pzGame: PZGame, pzRcon: PZRcon):
        self.pz_exe_path = app_config['pz']['pz_exe_path']
        self.pzGame = pzGame
        self.pzRcon = pzRcon
        self.steamcmd = steamcmd
        self.check_start()

    def check_start(self):
        if self.pzGame.is_process_running():
            print("Server Running")
            if self.pzRcon.check_open():
                print("Server Started")

    def check_if_server_installed(self):
        if not os.path.exists(f'{self.pz_exe_path}'):
            print(f'Installing PZ Dedicated Server to {self.pz_exe_path}')
            self.steamcmd.install_gamefiles(380870, self.pz_exe_path)
