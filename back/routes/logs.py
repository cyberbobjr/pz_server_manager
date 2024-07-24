import json
import os
from typing import Optional

from fastapi import APIRouter, Body
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from pz_setup import pzLog

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class LogSearchRequest(BaseModel):
    player: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    log_type: Optional[str] = None


@router.get("/logs/list_files", tags=["logs"])
async def list_files():
    file_list = []

    for root, dirs, files in os.walk(pzLog.path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return {
        "success": True,
        "msg": file_list
    }


@router.post("/logs/search", tags=["logs"])
async def search_logs(request: LogSearchRequest):
    result = pzLog.search_logs(
        player=request.player,
        start_date=request.start_date,
        end_date=request.end_date,
        log_type=request.log_type
    )
    return {
        "success": True,
        "msg": result
    }


@router.get("/logs/get_players", tags=["logs"])
async def get_all_players():
    players = pzLog.get_all_players()
    return {
        "success": True,
        "msg": list(players)
    }
