import os


class Bootstrap:
    @staticmethod
    def is_pzserver_ready(pzGame, pzRcon):
        return pzGame.is_process_running() and pzRcon.check_open()

    @staticmethod
    def is_pzserver_installed(pz_exe_path):
        if os.path.exists(f'{pz_exe_path}\\java\\zombie\\network\\GameServer.class'):
            return True
        return False

    @staticmethod
    def install_pzserver(pz_exe_path, steamcmd):
        print(f'Installing PZ Dedicated Server to {pz_exe_path}')
        steamcmd.install_gamefiles(380870, pz_exe_path)
