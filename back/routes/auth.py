import datetime
import jwt
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel

from libs import Config

router = APIRouter()


class Token(BaseModel):
    token: str


@router.post("/auth/login", tags=["auth"])
def login(username: str = Body(), password: str = Body()) -> Token:
    message = 'Incorrect credentials'
    try:
        if username == Config.app_config["auth"]["username"] and password == Config.app_config["auth"]["password"]:
            secret = Config.app_config['auth']['secret']
            payload = {
                'username': username,
                'expireIn': (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%s")
            }
            return Token(token=jwt.encode(payload, secret, algorithm='HS256'))
        raise HTTPException(status_code=401, detail=message)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail=message)
