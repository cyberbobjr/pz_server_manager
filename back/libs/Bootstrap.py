import os

from libs.PZGame import PZGame
from libs.PZRcon import PZRcon


class Bootstrap:
    @staticmethod
    def is_pzserver_ready(pzGame: PZGame, pzRcon: PZRcon):
        if pzGame.is_process_running():
            print("Server Running")
            if pzRcon.check_open():
                print("Server Started")
                return True
        return False

    @staticmethod
    def is_pzserver_installed(pz_exe_path):
        if os.path.exists(f'{pz_exe_path}\\java\\zombie\\network\\GameServer.class'):
            return True
        return False

    @staticmethod
    def install_pzserver(pz_exe_path, steamcmd):
        print(f'Installing PZ Dedicated Server to {pz_exe_path}')
        steamcmd.install_gamefiles(380870, pz_exe_path)
