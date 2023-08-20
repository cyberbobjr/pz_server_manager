import uvicorn
import os

from starlette.middleware.cors import CORSMiddleware

from libs.Config import init_config
from fastapi import FastAPI

from libs.Steam import Steam
from libs.SteamcmdException import Steamcmd
from routes import auth, console, mods

# steamcmd.install_workshopfiles(108600, 1510950729, os.path.abspath('test'))

CONF_FILE = "config.yml"
app_config = init_config(CONF_FILE)
steamcmd_path = os.path.join(app_config["steam"]["steamcmd_path"])
steamcmd = Steamcmd(steamcmd_path)
steam = Steam(app_config["steam"]["apikey"], app_config["steam"]["cache_folder"])

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
app.include_router(auth.router)
app.include_router(console.router)
app.include_router(mods.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
