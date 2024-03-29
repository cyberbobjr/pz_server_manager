import uvicorn
import os

from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from libs.Config import init_config
from fastapi import FastAPI

from libs.PZGame import PZGame
from libs.Steam import Steam
from libs.SteamcmdException import Steamcmd
from routes import auth, console, mods, appsteam

CONF_FILE = "config.yml"
app_config = init_config(CONF_FILE)
steamcmd_path = os.path.join(app_config["steam"]["steamcmd_path"])
steamcmd = Steamcmd(steamcmd_path)
steam = Steam(app_config["steam"]["apikey"], app_config["steam"]["cache_folder"])
mod_path = app_config["pz"]["mod_path"]
modpack_path = app_config["steam"]["modpack_path"]
pzGame = PZGame(mod_path, app_config["server"]["debug"])

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
app.include_router(auth.router)
app.include_router(console.router)
app.include_router(mods.router)
app.include_router(appsteam.router)
app.mount("/static", StaticFiles(directory=os.path.abspath(modpack_path)), name="static")
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
