import datetime

import jwt
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from pz_setup import app_config

router = APIRouter()


class Token(BaseModel):
    token: str


@router.post("/auth/login", tags=["auth"])
def login(username: str = Body(), password: str = Body()) -> Token:
    message = 'Incorrect credentials'
    try:
        if username == app_config["auth"]["username"] and password == app_config["auth"]["password"]:
            secret = app_config['auth']['secret']
            expire_at = datetime.datetime.now() + datetime.timedelta(days=1)
            payload = {
                'username': username,
                'expireIn': expire_at.timestamp()
            }
            return Token(token=jwt.encode(payload, secret, algorithm='HS256'))
        raise HTTPException(status_code=401, detail=message)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail=message)
