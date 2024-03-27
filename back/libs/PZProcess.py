import logging

import psutil

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class PZProcess:
    def __init__(self, pz_exe_path, pzMonitoring):
        self.pz_exe_path = pz_exe_path
        self.pzMonitoring = pzMonitoring

    def get_process(self):
        if not self.pzMonitoring:
            return None
        logging.debug("Recherche du processus de Project Zomboid en cours...")
        for process in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                arguments = psutil.Process(process.pid).cmdline()
                if process.name() == "java.exe" and 'zombie.network.GameServer' in arguments:
                    logging.debug(f"Processus trouvé : {process.name()}")
                    return process
                if process.name() == "cmd.exe" and f'{self.pz_exe_path}\\StartServer64.bat' in arguments:
                    logging.debug(f"Processus trouvé : {process.name()}")
                    return process
                if process.name() == "ProjectZomboid64":
                    logging.debug(f"Processus trouvé : {process.name()}")
                    return process
                if process.name() == "ProjectZomboid32":
                    logging.debug(f"Processus trouvé : {process.name()}")
                    return process
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                logging.error(f"Erreur lors de l'accès au processus {process.pid}: {e}")
        logging.debug("Aucun processus de Project Zomboid correspondant trouvé.")
        return None

    def get_pid(self):
        process = self.get_process()
        if process is not None:
            return process.pid
        logging.debug("Aucun PID trouvé pour un processus de Project Zomboid.")
        return None

    def get_running_time(self):
        process = self.get_process()
        if process is None:
            logging.debug("Impossible de récupérer le temps d'exécution : aucun processus de Project Zomboid trouvé.")
            return None
        return process.create_time()
