import asyncio
import uvicorn
import os

from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from libs.Bootstrap import Bootstrap
from libs.Config import init_config
from fastapi import FastAPI

from libs.PZGame import PZGame
from libs.Rcon import PZRcon
from libs.Steam import Steam
from libs.SteamcmdException import Steamcmd, SteamcmdException

from routes import auth, server, mods

global pz_process

CONF_FILE = "config.yml"
app_config = init_config(CONF_FILE)

steamcmd_path = os.path.join(app_config["steam"]["steamcmd_path"])
pz_exe_path = app_config["pz"]["pz_exe_path"]
server_path = app_config["pz"]["server_path"]

# check dirs
if not os.path.isdir(steamcmd_path):
    os.mkdir(steamcmd_path)
steamcmd = Steamcmd(steamcmd_path)
try:
    steamcmd.install()
except SteamcmdException as e:
    print(e)

# install if necessary

steam = Steam(app_config["steam"]["apikey"], app_config["steam"]["cache_folder"], app_config["steam"]["appid"])
pzGame = PZGame(pz_exe_path, server_path)
pzRcon = PZRcon(app_config["rcon"]["host"], app_config["rcon"]["port"], app_config["rcon"]["password"])

bootstrap = Bootstrap(app_config, steamcmd, pzGame, pzRcon)
bootstrap.check_if_server_installed()

app = FastAPI()


async def monitor_process():
    global pz_process
    while True:
        if not pzGame.is_process_running() and pzGame.should_be_always_start():
            pz_process = pzGame.start_server()
            print("Starting server")
        await asyncio.sleep(120)  # check every 2 minutes


@app.on_event("startup")
async def startup_db_client():
    print("startup")
    asyncio.create_task(monitor_process())


app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.include_router(auth.router)
app.include_router(server.router)
app.include_router(mods.router)
# app.mount("/static", StaticFiles(directory=os.path.abspath(modpack_path)), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=app_config["server"]["port"])
