import os
import json
import configparser
import re


def get_subdirectories(directory):
    subdirectories = []
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                subdirectories.append(item)
        return subdirectories
    except Exception as e:
        print("Une erreur s'est produite :", e)
        return []


def build_server_ini_file(packname, mod_ids: list[str]):
    filename = os.path.join(packname, "server.ini")
    config = configparser.ConfigParser()
    value = ";".join(mod_ids)
    if config.read(filename):
        if "Mods" in config:
            existing_values = config["Mods"]["Mods"]
            new_values = existing_values + ";" + value
            config["Mods"]["Mods"] = new_values
    else:
        config["Mods"] = {"Mods": value}
    with open(filename, "w") as config_file:
        config.write(config_file)


def build_modpack_info(packname, pack_info):
    modpack_info_path = os.path.join(packname, "modpackinfo.json")
    if os.path.exists(modpack_info_path):
        with open(modpack_info_path, 'r+') as modpack_info:
            existing = json.load(modpack_info)
            modpack_info.close()
        with open(modpack_info_path, 'w') as modpack_info:
            json.dump({**existing, **pack_info}, modpack_info, indent=4)
    else:
        with open(modpack_info_path, "w") as modpack_info:
            json.dump(pack_info, modpack_info, indent=4)


def parse_mod_info(file) -> str:
    modId = None
    with open(file) as f:
        try:
            for line in f:
                if line.startswith("id"):
                    modId = line.split("=")[1].strip()
            if modId is not None:
                return modId
        except:
            print(f"Error reading file {file}")


def modify_mod_info(file_path, prefix):
    with open(file_path, 'r') as file:
        content = file.read()
    # Recherche du motif id=xxxxxx dans le contenu du fichier
    lines = content.split('\n')
    new_lines = []
    old_id = None
    for line in lines:
        match_id = re.search(r'id=(.*)', line)
        match_name = re.search(r'name=(.*)', line)
        match_require = re.search(r'require=(.*)', line)
        if match_id:
            old_id = match_id.group(1)
            if prefix not in old_id:
                new_id = f'{prefix}{old_id}'
                line = line.replace(f'id={old_id}', f'id={new_id}')
        if match_name:
            old_name = match_name.group(1)
            if prefix not in old_name:
                new_name = f'{prefix}{old_name}'
                line = line.replace(f'name={old_name}', f'name={new_name}')
        if match_require:
            old_require = match_require.group(1)
            old_requires = old_require.split(',')
            requires = []
            for require in old_requires:
                if prefix not in require:
                    requires.append(prefix + require)
                else:
                    requires.append(require)
            line = "require=" + ",".join(requires)
        new_lines.append(line)
    # Écriture du contenu modifié dans le fichier
    with open(file_path, 'w') as file:
        file.write('\n'.join(new_lines))
    return old_id
