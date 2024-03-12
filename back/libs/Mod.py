import glob
import os
from pathlib import Path

REGEX_IMPORTS = "\\s*imports(.*)\\s+\\{([^}]+)\\}"
REGEX_RECIPE = "\\s*recipe (.*)\\s+\\{([^}]+)\\}"
REGEX_MODULE = "\\s*module (.*)$"
EXT = ".txt"
MODINFO = "mod.info"


class Mod:
    id = str
    maps = []

    def __init__(self, workshop_id, name, file):
        self.workshopId = workshop_id
        self.name = name
        self.path = os.path.dirname(file)
        self.file = file
        self.id = None

    def __str__(self):
        return f"{self.workshopId} / {self.id} => {self.name} ({self.path})"

    @staticmethod
    def get_modids_from_workshop_id(workshop_id, mod_path: str):
        ids = []
        if os.path.exists(f'{mod_path}\\{workshop_id}'):
            for file in glob.glob(f'{mod_path}\\{workshop_id}*\\mods\\*\\{MODINFO}'):
                mod_id = Mod.read_id_from_mod_info_file(file)
                if mod_id is not None:
                    ids.append(mod_id)
        return ids

    def get_mapids_from_workshop_id(workshop_id, mod_path: str):
        workshop_path = f'{mod_path}\\{workshop_id}'
        if os.path.exists(workshop_path):
            base_path = Path(workshop_path)
            maps_dirs = base_path.rglob("media/maps/*")  # Modifier pour chercher dans "media/maps"
            map_ids = []
            for maps_dir in maps_dirs:
                if maps_dir.is_dir():  # Vérifie que le chemin est bien un répertoire
                    map_ids.append(maps_dir.name)  # Ajoute le nom du répertoire à la liste
            return map_ids
        return []

    @staticmethod
    def read_id_from_mod_info_file(file):
        try:
            with open(file, 'rb') as modinfo_content:
                for line in modinfo_content:
                    if line.startswith(b"id"):
                        return line.split(b"=")[1].strip()
            return None
        except Exception as e:
            print(e)

    @staticmethod
    def convert_modinfo_to_json(modinfo_content, modname):
        modinfo_json = {}
        for line in modinfo_content:
            line = line.strip().replace("\n", "")
            try:
                if len(line) > 1:
                    if line.startswith("require"):
                        modinfo_json["require"] = line.replace("require=", "").split(",")
                    elif line.startswith("url"):
                        modinfo_json["url"] = line.replace("url=", "")
                    else:
                        key, value = line.split("=")
                        modinfo_json[key] = value
            except Exception as e:
                if 'description' in modinfo_json:
                    modinfo_json['description'] += '\n' + line
                else:
                    modinfo_json['description'] = line
        modinfo_json["dir"] = modname
        return modinfo_json
