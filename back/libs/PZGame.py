import glob
import os
import re
import subprocess

import psutil

from .Mod import Mod
from .PZConfigFile import PZConfigFile

MODINFO = "mod.info"


class PZGame:
    mods: list[Mod] = []
    mod_path = "\\steamapps\\workshop\\content\\108600\\"
    server_path = ""
    pz_exe_path = ""
    server_name = "servertest"
    pz_config: PZConfigFile

    def __init__(self, pz_exe_path: str, server_path: str):
        self.must_restart = True
        self.init(pz_exe_path, server_path)

    def init(self, pz_exe_path: str, server_path: str):
        self.pz_exe_path = pz_exe_path
        self.server_path = server_path
        self.pz_config = PZConfigFile(self.server_path + '\\' + self.server_name + '.ini')

    def scan_mods_in_server_dir(self):
        self.mods = []
        for file in glob.glob(f'{self.pz_exe_path}{self.mod_path}*\\mods\\*\\{MODINFO}'):
            mod = self.parse_info(file)
            if mod is not None:
                self.mods.append(mod)

    def scan_mods_in_ini(self):
        mods = self.read_mods_ini()
        workshops = self.read_workshops_ini()
        return [mods, workshops]

    def read_mods_ini(self):
        return self.pz_config.get_value("Mods").split(";")

    def read_workshops_ini(self):
        return self.pz_config.get_value("WorkshopItems").split(";")

    def parse_info(self, file) -> Mod:
        workshop_id = None
        name = None
        mod_id = None
        pz_mod_path = f'{self.pz_exe_path}{self.mod_path}'
        with open(file) as f:
            try:
                for line in f:
                    if line.startswith("name"):
                        workshop_id = file[len(pz_mod_path):].split(os.path.sep)[0]
                        name = line.split("=")[1].strip()
                    if line.startswith("id"):
                        mod_id = line.split("=")[1].strip()
                if workshop_id is not None and name is not None and mod_id is not None:
                    mod = Mod(workshop_id, name, file)
                    mod.id = mod_id
                    return mod
            except:
                print(f"Error reading file {file}")

    def display_mods_infos(self):
        for mod in self.mods:
            print(mod)

    def build_server_mods_ini(self, Mods, WorkshopItems):
        ini_path = f'{self.server_path}\\{self.server_name}.ini'
        with open(ini_path, 'r') as file:
            lines = file.readlines()
            # Parcourir les lignes du fichier pour trouver et remplacer la chaîne
            for i, line in enumerate(lines):
                if re.match(r'\s*Mods\s*=', line):
                    # Construire la nouvelle ligne avec les valeurs fournies
                    new_line = "Mods=" + ';'.join(Mods) + "\n"
                    # Remplacer la ligne dans la liste des lignes
                    lines[i] = new_line
                if re.match(r'\s*WorkshopItems\s*=', line):
                    # Construire la nouvelle ligne avec les valeurs fournies
                    new_line = "WorkshopItems=" + ';'.join(WorkshopItems) + "\n"
                    # Remplacer la ligne dans la liste des lignes
                    lines[i] = new_line

        # Réécrire le fichier avec les lignes modifiées
        with open(ini_path, 'w') as file:
            file.writelines(lines)

    def build_server_ini(self, key: str, value):
        ini_path = f'{self.server_path}\\{self.server_name}.ini'
        with open(ini_path, 'r') as file:
            lines = file.readlines()
            # Parcourir les lignes du fichier pour trouver et remplacer la chaîne
            for i, line in enumerate(lines):
                if re.match(rf'\s*{key.strip()}\s*=', line):
                    # Construire la nouvelle ligne avec les valeurs fournies
                    new_line = f"{key.strip()}=" + value
                    # Remplacer la ligne dans la liste des lignes
                    lines[i] = new_line

        # Réécrire le fichier avec les lignes modifiées
        with open(ini_path, 'w') as file:
            file.writelines(lines)

        return lines

    def is_process_running(self) -> bool:
        return self.get_pid() is not None

    def get_pid(self):
        for process in psutil.process_iter():
            try:
                arguments = psutil.Process(process.pid).cmdline()
                if process.name() == "java.exe" and 'zombie.network.GameServer' in arguments:
                    return process.pid
                if process.name() == "cmd.exe" and f'{self.pz_exe_path}\\StartServer64.bat' in arguments:
                    return process.pid
            except Exception as e:
                continue
        return None

    def start_server(self):
        from main import app_config
        if "log_filename" not in app_config["pz"]:
            app_config["pz"]["log_filename"] = "output.txt"
        output_file_name = app_config["pz"]["log_filename"]
        process_path = f'{self.get_exe_path()}\\StartServer64.bat > {output_file_name}'
        return subprocess.Popen(process_path,
                                cwd=self.get_exe_path(),
                                creationflags=subprocess.CREATE_NEW_CONSOLE)

    async def stop_server(self):
        from main import pzRcon
        return await pzRcon.send_command("quit")

    def should_be_always_start(self):
        return self.must_restart

    def set_be_always_start(self, state: bool):
        self.must_restart = state

    def get_exe_path(self) -> str:
        return f'{self.pz_exe_path}'

    def get_mod_path(self) -> str:
        return f'{self.pz_exe_path}{self.mod_path}'
