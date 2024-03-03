import psutil


class PZProcess:
    def __init__(self, pz_exe_path):
        self.pz_exe_path = pz_exe_path

    def get_process(self):
        for process in psutil.process_iter(['pid', 'name']):
            try:
                psutil.Process(process.pid)
                arguments = psutil.Process(process.pid).cmdline()
                if process.name() == "java.exe" and 'zombie.network.GameServer' in arguments:
                    return process
                if process.name() == "cmd.exe" and f'{self.pz_exe_path}\\StartServer64.bat' in arguments:
                    return process
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return None

    def get_pid(self):
        process = self.get_process()
        if process is not None:
            return process.pid
        return None

    def get_running_time(self):
        process = self.get_process()
        if process is None:
            return None
        return process.create_time()
