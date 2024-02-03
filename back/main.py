import uvicorn
import os

from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from libs.Config import init_config
from fastapi import FastAPI

from libs.PZGame import PZGame
from libs.Rcon import PZRcon
from libs.Steam import Steam
from libs.SteamcmdException import Steamcmd, SteamcmdException

from routes import auth, server, mods

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

steam = Steam(app_config["steam"]["apikey"], app_config["steam"]["cache_folder"], app_config["steam"]["appid"])
pzGame = PZGame(pz_exe_path, server_path)
pzRcon = PZRcon(app_config["rcon"]["host"], app_config["rcon"]["port"], app_config["rcon"]["password"])

if pzGame.check_process():
    print("Server Running")

if pzRcon.check_open():
    print("Server Started")

app = FastAPI()
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
