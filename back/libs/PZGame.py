import glob
import os

import psutil

from .Mod import Mod
from .PZConfigFile import PZConfigFile

MODINFO = "mod.info"


class PZGame:
    mods: list[Mod] = []
    server_path = ""
    pz_exe_path = ""
    server_name = "servertest"
    pz_config: PZConfigFile

    def __init__(self, pz_exe_path: str, server_path: str):
        self.init(pz_exe_path, server_path)

    def init(self, pz_exe_path: str, server_path: str):
        self.pz_exe_path = pz_exe_path
        self.server_path = server_path
        self.pz_config = PZConfigFile(self.server_path + '\\' + self.server_name + '.ini')

    def scan_mods_in_server_dir(self):
        self.mods = []
        for file in glob.glob(f'{self.pz_exe_path}\\steamapps\\workshop\\content\\108600\\*\\mods\\*\\{MODINFO}'):
            mod = self.parse_info(file)
            if mod is not None:
                self.mods.append(mod)

    def read_mods_ini(self):
        return self.pz_config.get_value("Mods").split(";")

    def read_workshops_ini(self):
        return self.pz_config.get_value("WorkshopItems").split(";")

    def parse_info(self, file) -> Mod:
        workshop_id = None
        name = None
        mod_id = None
        pz_mod_path = f'{self.pz_exe_path}\\steamapps\\workshop\\content\\108600\\'
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

    def build_server_test_file(self):
        workshop_items = []
        mod_ids = []
        f = open("server.ini", "w")
        for mod in self.mods:
            workshop_items.append(mod.workshopId)
            mod_ids.append(mod.id)
        f.write("WorkshopItems=" + ";".join(workshop_items) + "\n")
        f.write("Mods=" + ";".join(mod_ids))
        f.close()

    def export_all_mods(self):
        f = open("mods.txt", "w")
        for mod in self.mods:
            f.write(f"{mod.name}\n")
        f.close()

    def check_process(self) -> bool:
        return self.get_pid() is not None

    def get_pid(self):
        for process in psutil.process_iter():
            try:
                arguments = psutil.Process(process.pid).cmdline()
                if process.name() == "java.exe" and 'zombie.network.GameServer' in arguments:
                    return process.pid
            except:
                continue
        return None
