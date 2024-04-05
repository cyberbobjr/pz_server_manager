import json
import os
import shutil
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from setuptools import glob

from libs.modpack_utils import modify_mod_info
from pz_setup import app_config, steam, steamcmd

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

"""
WIP modpack management
This class will manage modpack for server (scan, build, check for update)
"""


class WorkshopOrderRequest(BaseModel):
    packname: str
    workshop_id: str
    new_position: int


class ModOrderRequest(BaseModel):
    packname: str
    workshop_id: str
    mod_id: str
    new_position: int


class ModAddRequest(BaseModel):
    packname: str
    workshopIds: list[str]  # Liste d'ID de workshop


class ModpackCreateRequest(BaseModel):
    packname: str
    prefix: str


class ModToggleRequest(BaseModel):
    packname: str  # Nom du modpack
    workshop_id: str  # ID du workshop Steam pour le mod
    mod_id: str  # ID du mod à toggler
    enabled: bool  # État cible (True pour activer, False pour désactiver)


@router.post("/modpack/change_workshop_order", tags=["modpack"])
async def change_workshop_order(request: WorkshopOrderRequest):
    dst_packname = os.path.join(app_config["steam"]["modpack_path"], request.packname)
    modpack_info_path = os.path.join(dst_packname, "modpackinfo.json")

    if not os.path.exists(modpack_info_path):
        raise HTTPException(status_code=404, detail="Modpack does not exist")

    with open(modpack_info_path) as f:
        modpack_info = json.load(f)

    mods_list = modpack_info.get("mods", [])
    workshop_index = next((i for i, item in enumerate(mods_list) if item["workshop_id"] == request.workshop_id), None)

    if workshop_index is None:
        raise HTTPException(status_code=404, detail="Workshop ID not found in modpack.")

    # Reorder the workshop_id
    workshop_item = mods_list.pop(workshop_index)
    mods_list.insert(request.new_position, workshop_item)

    modpack_info["mods"] = mods_list
    modpack_info["last_updated"] = datetime.now().isoformat()

    with open(modpack_info_path, "w") as f:
        json.dump(modpack_info, f, indent=4)

    return {"message": "Workshop order updated successfully."}


@router.post("/modpack/change_mod_order", tags=["modpack"])
async def change_mod_order(request: ModOrderRequest):
    dst_packname = os.path.join(app_config["steam"]["modpack_path"], request.packname)
    modpack_info_path = os.path.join(dst_packname, "modpackinfo.json")

    if not os.path.exists(modpack_info_path):
        raise HTTPException(status_code=404, detail="Modpack or modpack info file not found.")

    with open(modpack_info_path, "r") as f:
        modpack_info = json.load(f)

    # Vérification de l'existence du workshop_id et du mod_id
    if request.workshop_id in modpack_info["mods"]:
        mods_list = modpack_info["mods"][request.workshop_id]["modIds"]
        mod_index = next((index for (index, d) in enumerate(mods_list) if d["id"] == request.mod_id), None)

        # Vérifier si le mod_id a été trouvé
        if mod_index is None:
            raise HTTPException(status_code=404, detail="Specified mod_id not found in the modpack.")

        # Changement de l'ordre du mod_id
        mod_to_move = mods_list.pop(mod_index)
        mods_list.insert(request.new_position, mod_to_move)
        modpack_info["last_updated"] = datetime.now().isoformat()

        with open(modpack_info_path, "w") as f:
            json.dump(modpack_info, f, indent=4)

        return {"message": "Mod order updated successfully."}
    else:
        raise HTTPException(status_code=404, detail="Specified workshop_id not found in the modpack.")


@router.get("/modpack/{packname}/mods", tags=["modpack"])
async def get_mod_ids(packname: str):
    dst_packname = os.path.join(app_config["steam"]["modpack_path"], packname)
    modpack_info_path = os.path.join(dst_packname, "modpackinfo.json")

    # Vérifier si le modpack et son fichier d'info existent
    if not os.path.exists(modpack_info_path):
        raise HTTPException(status_code=404, detail="Modpack or modpack info file not found.")

    # Lire les informations du modpack
    with open(modpack_info_path, "r") as f:
        modpack_info = json.load(f)

    # Collecter tous les mod_id activés
    mod_ids = []
    for mod_data in modpack_info["mods"]:  # mod_data est directement le dictionnaire de chaque mod
        for mod in mod_data["modIds"]:
            if mod.get("enabled", True):
                mod_ids.append(mod["id"])

    # Joindre les mod_id avec des points-virgules pour le retour
    mods_string = ";".join(mod_ids)

    return {"mods": mods_string}


@router.get("/modpacks", tags=["modpack"])
async def list_modpacks(details: Optional[bool] = Query(default=False)):
    modpack_path = app_config["steam"]["modpack_path"]
    modpacks = os.listdir(modpack_path)

    modpack_list = []
    for modpack in modpacks:
        modpack_dir = os.path.join(modpack_path, modpack)
        modpack_info_path = os.path.join(modpack_dir, "modpackinfo.json")

        if os.path.exists(modpack_info_path):
            with open(modpack_info_path, "r") as f:
                modpack_info = json.load(f)

                # Récupérer les détails des mods si demandé
                if details and "mods" in modpack_info:
                    workshop_ids = [mod["workshop_id"] for mod in modpack_info["mods"]]
                    mod_details = steam.get_mod_info(workshop_ids)
                    for mod in modpack_info["mods"]:
                        if mod["workshop_id"] in mod_details:
                            mod["details"] = mod_details[mod["workshop_id"]]

                modpack_list.append({
                    "name": modpack,
                    "info": modpack_info
                })
        else:
            modpack_list.append({
                "name": modpack,
                "info": "No modpackinfo.json found"
            })

    return modpack_list


@router.post("/modpack/create", tags=["modpack"])
async def create_modpack(request: ModpackCreateRequest):
    packname = request.packname
    prefix = request.prefix  # Récupérer le préfixe à partir de la requête
    dst_packname = os.path.join(app_config["steam"]["modpack_path"], packname)

    if os.path.exists(dst_packname):
        raise HTTPException(status_code=400, detail="Modpack already exists")

    os.makedirs(dst_packname)

    modpack_info = {
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "mods": [],
        "prefix": prefix  # Enregistrer le préfixe dans la configuration du modpack
    }

    with open(os.path.join(dst_packname, "modpackinfo.json"), "w") as f:
        json.dump(modpack_info, f, indent=4)

    return {"message": f"Modpack '{packname}' created successfully."}


@router.delete("/modpack/{packname}", tags=["modpack"])
async def delete_modpack(packname: str):
    dst_packname = os.path.join(app_config["steam"]["modpack_path"], packname)

    # Vérifier si le répertoire du modpack existe
    if not os.path.exists(dst_packname):
        raise HTTPException(status_code=404, detail="Modpack not found.")

    # Effacer le répertoire du modpack et son contenu
    try:
        shutil.rmtree(dst_packname)
        return {"message": f"Modpack '{packname}' has been successfully deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting modpack '{packname}': {e}")


@router.post("/modpack/add_mods", tags=["modpack"])
async def build_pack(request: ModAddRequest):
    packname = request.packname
    dst_packname = os.path.join(app_config["steam"]["modpack_path"], packname)
    modpack_info_path = os.path.join(dst_packname, "modpackinfo.json")

    if not os.path.exists(dst_packname) or not os.path.exists(modpack_info_path):
        raise HTTPException(status_code=404, detail="Modpack does not exist")

    with open(modpack_info_path, "r") as f:
        modpack_info = json.load(f)

    mods_list = modpack_info.get("mods", [])
    prefix = modpack_info.get("prefix", "")

    for workshop_id in request.workshopIds:
        # Assurez-vous que la logique de téléchargement et de copie est correctement gérée ici.
        dst_dir = os.path.abspath(os.path.join(dst_packname, workshop_id))
        src_dir = os.path.join(app_config["steam"]["steamcmd_path"], "steamapps", "workshop", "content",
                               str(app_config["steam"]["appid"]), workshop_id)

        if not os.path.exists(src_dir):
            print(f"Téléchargement du mod {workshop_id}")
            # Utilisez steamcmd pour télécharger le mod
            steamcmd.install_workshopfiles(
                gameid=108600,
                workshop_id=workshop_id,
                game_install_dir=None,
                user='anonymous',  # Utilisez les paramètres nécessaires pour votre cas
                validate=True  # ou False, selon le besoin
            )
            # Copie du mod dans la destination
        if os.path.exists(src_dir):
            # Copier le contenu du répertoire et de ses sous-répertoires dans packname
            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

        workshop_mod = next((item for item in mods_list if item["workshop_id"] == workshop_id), None)
        if not workshop_mod:
            workshop_mod = {"workshop_id": workshop_id, "modIds": [], "last_updated": datetime.now().isoformat()}
            mods_list.append(workshop_mod)

        mod_info_files = glob.glob(os.path.join(dst_packname, workshop_id, "**", "mod.info"), recursive=True)
        for mod_info_path in mod_info_files:
            mod_id = modify_mod_info(mod_info_path, prefix + "_")
            mod_obj = {"id": prefix + "_" + mod_id, "enabled": True}
            if all(mod_obj["id"] != mod["id"] for mod in workshop_mod["modIds"]):
                workshop_mod["modIds"].append(mod_obj)

    modpack_info["mods"] = mods_list
    modpack_info["last_updated"] = datetime.now().isoformat()

    with open(modpack_info_path, "w") as f:
        json.dump(modpack_info, f, indent=4)

    return {"message": f"Le pack '{packname}' a été construit avec succès."}


@router.post("/modpack/toggle_mod", tags=["modpack"])
async def toggle_mod_in_modpack(request: ModToggleRequest):
    packname = request.packname
    workshop_id = request.workshop_id
    mod_id_to_toggle = request.mod_id
    enabled = request.enabled

    dst_packname = os.path.join(app_config["steam"]["modpack_path"], packname)
    modpack_info_path = os.path.join(dst_packname, "modpackinfo.json")

    if not os.path.exists(modpack_info_path):
        raise HTTPException(status_code=404, detail="Modpack does not exist or modpack info file missing.")

    with open(modpack_info_path, "r") as f:
        modpack_info = json.load(f)

    # Trouver le workshop_id dans la liste
    workshop_mod = next((item for item in modpack_info["mods"] if item["workshop_id"] == workshop_id), None)

    if workshop_mod:
        mod_found = False
        # Itérer sur les modIds pour trouver le mod_id spécifié
        for mod in workshop_mod["modIds"]:
            if mod["id"] == mod_id_to_toggle:
                mod["enabled"] = enabled
                mod_found = True
                break
        if not mod_found:
            raise HTTPException(status_code=404, detail="Specified mod_id not found in the modpack.")
    else:
        raise HTTPException(status_code=404, detail="Specified workshop_id not found in the modpack.")

    modpack_info["last_updated"] = datetime.now().isoformat()

    with open(modpack_info_path, "w") as f:
        json.dump(modpack_info, f, indent=4)

    return {
        "message": f"Mod '{mod_id_to_toggle}' in modpack '{packname}' has been {'enabled' if enabled else 'disabled'}."}


@router.get("/modpack/{packname}/check_updates", tags=["modpack"])
async def check_modpack_updates(packname: str):
    dst_packname = os.path.join(app_config["steam"]["modpack_path"], packname)
    modpack_info_path = os.path.join(dst_packname, "modpackinfo.json")

    if not os.path.exists(modpack_info_path):
        raise HTTPException(status_code=404, detail="Modpack does not exist.")

    with open(modpack_info_path, "r") as f:
        modpack_info = json.load(f)

    updated_mods = []
    workshop_ids = [mod["workshop_id"] for mod in modpack_info["mods"]]
    mod_details = steam.get_mod_info(workshop_ids)

    for workshop_mod in modpack_info["mods"]:
        workshop_id = workshop_mod["workshop_id"]
        if workshop_id in mod_details:
            detail = mod_details[workshop_id]
            if "time_updated" in detail:
                steam_update_time = datetime.utcfromtimestamp(detail["time_updated"])
                modpack_update_time = datetime.strptime(workshop_mod["last_updated"], "%Y-%m-%dT%H:%M:%S.%f")

                if steam_update_time > modpack_update_time:
                    updated_mods.append(workshop_id)

    return {"updated_mods": updated_mods}
                          