from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from libs.Mod import Mod

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class SearchModRequest(BaseModel):
    tags: Optional[list[str]]
    cursor: Optional[str]
    text: Optional[str]


@router.get("/mods/", tags=["list mod"])
async def index(force=False):
    try:
        mods = []
        from main import pzGame
        pzGame.scan_mods_in_server_dir()
        from main import steam
        for mod in pzGame.mods:
            mod_info = open(mod.file, "r")
            mods.append({
                "mod_info": Mod.convert_modinfo_to_json(mod_info.readlines(), mod.path),
                "steam_data": steam.get_mod_info(mod.workshopId)
            })
        return mods
    except Exception as e:
        print(e)


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