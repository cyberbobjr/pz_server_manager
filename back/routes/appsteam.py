from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class SearchModRequest(BaseModel):
    tags: Optional[list[str]]
    cursor: Optional[str]
    text: Optional[str]


@router.get("/steam/latest", tags=['Get latest mods'])
async def get_latest():
    try:
        from main import steam
        mods = steam.search_mod()
        result = []
        for mod in mods['response']['publishedfiledetails']:
            result.append(steam.get_mod_info(mod['publishedfileid']))
        return result
    except Exception as e:
        print("Erreur :")
        print(e)


@router.post("/steam/search")
async def search_mods(request: SearchModRequest):
    try:
        cursor = request.cursor
        tags = request.tags
        text = request.text
        from main import steam
        mods = steam.search_mod(cursor, text, tags, sort=12)
        result = []
        for mod in mods['response']['publishedfiledetails']:
            result.append(steam.get_mod_info(mod['publishedfileid']))
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
