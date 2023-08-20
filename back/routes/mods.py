import json
import os
import re
import shutil
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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


def build_server_ini_file(packname, mod_ids: list[str]):
    f = open(os.path.join(packname, "server.ini"), "w")
    f.write("Mods=" + ";".join(mod_ids))
    f.close()


def build_modpack_info(packname, pack_info):
    with open(os.path.join(packname, "modpack.info"), "w") as modpack_info:
        json.dump(pack_info, modpack_info, indent=4)


def modify_mod_info(file_path, prefix):
    with open(file_path, 'r') as file:
        content = file.read()

    # Recherche du motif id=xxxxxx dans le contenu du fichier
    lines = content.split('\n')
    new_lines = []
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


def get_workshop_id(mod_path: str):
    from main import app_config
    root_mod_path = app_config["pz"]["mod_path"]
    workshop_id = mod_path[len(root_mod_path):].split(os.path.sep)[1]
    print(workshop_id)
    return workshop_id


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


class BuildPackRequest(BaseModel):
    mods: list[str]
    packname: str
    prefix: str


class SearchModRequest(BaseModel):
    tags: Optional[list[str]]
    cursor: Optional[str]
    text: Optional[str]


@router.get("/mods/", tags=["list mod"])
async def index(force=False):
    try:
        from main import pzGame
        pzGame.scan_mods()
        from main import steam
        for mod in pzGame.mods:
            mod.steam_data = steam.get_mod_info(mod.workshopId, force)
        return pzGame.mods
    except Exception as e:
        print(e)


@router.get("/mods/modpack")
async def get_build_pack(packname: str = None):
    from main import app_config
    from main import steam
    modpack_path = app_config["steam"]["modpack_path"]
    if packname is None:
        return get_subdirectories(modpack_path)
    with open(os.path.join(modpack_path, packname, "modpack.info"), "r") as cache_file:
        mods = {}
        modpack_content = json.load(cache_file)
        for key, mod in modpack_content.items():
            mods[key] = steam.get_mod_info(mod)
        return mods


@router.post("/mods/modpack")
async def build_pack(request: BuildPackRequest):
    try:
        pack_info = {}
        mods = request.mods
        packname = request.packname
        prefix = request.prefix
        from main import app_config
        dst_packname = os.path.join(app_config["steam"]["modpack_path"], packname)
        # Créer le répertoire du pack
        if not os.path.exists(dst_packname):
            os.makedirs(dst_packname)
        ids = []
        # Parcourir chaque répertoire dans mods et copier son contenu dans le répertoire packname
        for mod_dir in mods:
            workshop_id = get_workshop_id(mod_dir)
            mod_id = parse_mod_info(os.path.join(mod_dir, 'mod.info'))
            pack_info[mod_id] = workshop_id
            dst_dir = os.path.join(dst_packname, os.path.basename(mod_dir))
            if os.path.exists(mod_dir) and os.path.isdir(mod_dir) and not os.path.exists(dst_dir):
                # Copier le contenu du répertoire et de ses sous-répertoires dans packname
                shutil.copytree(mod_dir, dst_dir, dirs_exist_ok=True)
            mod_info_path = os.path.join(dst_packname, mod_id, "mod.info")
            if os.path.exists(mod_info_path):
                modify_mod_info(os.path.join(dst_packname, mod_id, "mod.info"), prefix)
                ids.append(prefix + mod_id)
            else:
                return HTTPException(status_code=400, detail=f"Le répertoire {mod_dir} n'existe pas.")
        build_server_ini_file(dst_packname, ids)
        build_modpack_info(dst_packname, pack_info)
        return {"message": f"Le pack '{packname}' a été construit avec succès."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mods/search")
async def search_mods(request: SearchModRequest):
    try:
        cursor = request.cursor
        tags = request.tags
        text = request.text
        from main import steam
        return steam.search_mod(cursor, text, tags)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mods/download")
async def search_mods(workshop_id: str):
    from main import steamcmd
    from main import app_config
    steamcmd.install_workshopfiles(app_config["steam"]["appid"], workshop_id, app_config["pz"]["mod_path"])
    return {"message": f"Le mod '{workshop_id}' a été téléchargé avec succès."}


@router.delete("/mods/modpack")
async def get_build_pack(packname: str, modname: str):
    from main import app_config
    modpack_path = os.path.join(app_config["steam"]["modpack_path"], packname)
    if not os.path.exists(modpack_path):
        raise HTTPException(status_code=404, detail="Le modpack n'existe pas")
    if not os.path.exists(os.path.join(modpack_path, modname)):
        raise HTTPException(status_code=404, detail="Le mod n'existe pas")
    with open(os.path.join(modpack_path, "modpack.info"), "r") as cache_file:
        modpack_content = json.load(cache_file)
        del modpack_content[modname]
    with open(os.path.join(modpack_path, "modpack.info"), "w") as cache_file:
        json.dump(modpack_content, cache_file, indent=4)
    shutil.rmtree(os.path.join(modpack_path, modname))
    mods = get_subdirectories(modpack_path)
    build_server_ini_file(modpack_path, mods)
    return modpack_content
