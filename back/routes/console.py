from fastapi import Body, APIRouter

from mcrcon import MCRcon
from libs import Config
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/console/command", tags=["console"])
async def command(cmd: str = Body()):
    port = Config.app_config["rcon"]["port"]
    password = Config.app_config["rcon"]["password"]
    host = Config.app_config["rcon"]["host"]
    try:
        with MCRcon(host, port=port, password=password) as client:
            # await client.connect()
            result = client.command(cmd)
            print(result)
            # await client.close()
            return result
    except Exception as e:
        print(e)
