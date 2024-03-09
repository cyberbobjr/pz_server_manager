from typing import Optional, List

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from libs.Mod import Mod
from pz_setup import pzGame, steam, app_config, steamcmd

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class SearchModRequest(BaseModel):
    tags: Optional[list[str]]
    cursor: Optional[str]
    text: Optional[str]


@router.get("/mods/installed", tags=["mods"])
async def index():
    try:
        mods = []
        pzGame.scan_mods_in_server_dir()
        for mod in pzGame.mods:
            mod_info = open(mod.file, "r")
            mods.append({
                "WorkshopItems": mod.workshopId,
                "Mods": mod.id,
                "mod_info": Mod.convert_modinfo_to_json(mod_info.readlines(), mod.path),
                "steam_data": steam.get_mod_info(mod.workshopId)
            })
        return mods
    except Exception as e:
        print(e)


@router.get("/mods/ini", tags=["mods"])
async def get_mod_ini():
    try:
        workshops = []
        [Mods, workshop_items] = pzGame.scan_mods_in_ini()
        for w in workshop_items:
            modids = Mod.get_modids_from_workshop_id(w, pzGame.get_mod_path())
            workshops.append({
                "Mods": modids,
                "WorkshopItems": w,
                "steam_data": steam.get_mod_info(w)
            })
        return {"success": True,
                "msg": {
                    "Mods_ini": Mods,
                    "Workshop_ini": workshop_items,
                    "workshop_items": workshops
                }
                }
    except Exception as e:
        print(e)
        return {
            "success": False,
            "msg": e
        }


@router.post("/mods/search", tags=["mods"])
async def search_mods(request: SearchModRequest):
    try:
        cursor = request.cursor
        tags = request.tags
        text = request.text
        return steam.search_mod(cursor, text, tags)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mods/download", tags=["mods"])
async def search_mods(workshop_id: str):
    try:
        steamcmd.install_workshopfiles(app_config["steam"]["appid"], workshop_id, pzGame.get_exe_path())
        return {"success": True, "message": f"The mod '{workshop_id}' was downloaded"}
    except Exception as e:
        print(e)
        return {"success": False, "message": f"Error {e}"}
