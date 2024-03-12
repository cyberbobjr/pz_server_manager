from typing import Optional, List

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from libs.Mod import Mod
from pz_setup import pzGame, steam, app_config, steamcmd
from typing import Dict, Tuple, Any
import time

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class SearchModRequest(BaseModel):
    tags: Optional[list[str]] = None
    cursor: Optional[str] = None
    text: Optional[str] = None


# Structure de cache: {(cursor, text, tags): (timestamp, result)}
CACHE: Dict[Tuple[Optional[str], Optional[str], Optional[Tuple[str]]], Tuple[float, Any]] = {}
CACHE_DURATION = 15 * 60  # 15 minutes en secondes


def cache_key(cursor: Optional[str], text: Optional[str], tags: Optional[list[str]]) -> Tuple[
    Optional[str], Optional[str], Optional[Tuple[str]]]:
    """Crée une clé de cache unique basée sur les paramètres de la requête."""
    # Gère les tags None comme une liste vide pour la cohérence de la clé
    sorted_tags = tuple(sorted(tags)) if tags else None
    return (cursor, text, sorted_tags)


def get_cached_result(key: Tuple[Optional[str], Optional[str], Optional[Tuple[str]]]) -> Any:
    """Renvoie le résultat mis en cache s'il est valide, sinon None."""
    if key in CACHE:
        timestamp, result = CACHE[key]
        if time.time() - timestamp < CACHE_DURATION:
            return result
    return None


def cache_result(key: Tuple[Optional[str], Optional[str], Optional[Tuple[str]]], result: Any):
    """Cache le résultat de la requête."""
    CACHE[key] = (time.time(), result)


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
            workshops.append({
                "Mods": Mod.get_modids_from_workshop_id(w, pzGame.get_mod_path()),
                "Maps": Mod.get_mapids_from_workshop_id(w, pzGame.get_mod_path()),
                "WorkshopItems": w,
                "steam_data": steam.get_mod_info(w)
            })
        return {
            "success": True,
            "msg": {
                "Mods_ini": Mods,
                "Workshop_ini": workshop_items,
                "Maps_ini": pzGame.read_maps_ini(),
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
        # Crée la clé de cache
        key = cache_key(cursor, text, tags)

        # Vérifie si le résultat est déjà dans le cache
        cached_result = get_cached_result(key)
        if cached_result is not None:
            cached_result['from_cache'] = True
            return cached_result

        # Si le résultat n'est pas dans le cache, exécute la recherche
        result = steam.search_mod(cursor, text, tags)

        # Met en cache le nouveau résultat
        cache_result(key, result)
        result['from_cache'] = False
        return result
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
