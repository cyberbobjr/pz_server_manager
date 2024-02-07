import asyncio
import time

import uvicorn
import os
import datetime
import signal

from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from libs.Bootstrap import Bootstrap
from libs.Config import init_config
from fastapi import FastAPI

from libs.PZDiscord import PZDiscord
from libs.PZGame import PZGame
from libs.PZLog import PZLog
from libs.Rcon import PZRcon
from libs.Steam import Steam
from libs.Steamcmd import Steamcmd, SteamcmdException

from routes import auth, server, mods

CONF_FILE = "config.yml"
app_config = init_config(CONF_FILE)

steamcmd_path = os.path.join(app_config["steam"]["steamcmd_path"])

# check dirs
if not os.path.isdir(steamcmd_path):
    os.mkdir(steamcmd_path)
steamcmd = Steamcmd(steamcmd_path)
try:
    steamcmd.install()
except SteamcmdException as e:
    print(e)

steam = Steam(app_config["steam"]["apikey"], app_config["steam"]["cache_folder"], app_config["steam"]["appid"])
pzGame = PZGame(app_config["pz"]["pz_exe_path"], app_config["pz"]["server_path"], app_config["pz"]["password"])
pzRcon = PZRcon(app_config["rcon"]["host"], app_config["rcon"]["port"], app_config["rcon"]["password"])
if app_config["discord"]["apikey"] and app_config["discord"]["channel"]:
    pzDiscord = PZDiscord(app_config["discord"]["apikey"], app_config["discord"]["channel"])
else:
    pzDiscord = None

bootstrap = Bootstrap(app_config, steamcmd, pzGame, pzRcon)
if not bootstrap.check_if_server_installed():
    PZLog.print(f'Relaunch the server...')
    exit(0)

app = FastAPI()


async def start_bot():
    await pzDiscord.run()


async def monitor_process():
    while True:
        if not pzGame.is_process_running() and pzGame.should_be_always_start():
            pzGame.start_server()
            await PZLog.print("Starting server")
        await asyncio.sleep(60 * 2)  # check every 2 minutes


async def monitor_mod_update():
    global pzGame, steam
    while True:
        [_, workshop_ids] = pzGame.scan_mods_in_ini()
        running_time = pzGame.get_process_running_time()
        msg = f'Server running since {epoch_to_iso(running_time)}'
        print(msg)
        if pzDiscord:
            await pzDiscord.send_message(msg)
        for workshop_id in workshop_ids:
            last_update = steam.get_lastupdate_mod(workshop_id)
            if last_update > running_time:
                msg = f'workshop item {workshop_id} was updated {epoch_to_iso(last_update)} since {epoch_to_iso(running_time)}, server rebooting'
                await PZLog.print(msg)
                await pzGame.stop_server()
                while pzGame.is_process_running():
                    time.sleep(5)
                pzGame.start_server()
                pzGame.set_be_always_start(True)
                break
        await asyncio.sleep(60 * 60)  # check every hour


def epoch_to_iso(epoch_time):
    try:
        # Convertir l'epoch en datetime
        dt_object = datetime.datetime.utcfromtimestamp(epoch_time)

        # Formater la date et l'heure au format ISO 8601
        iso_formatted = dt_object.strftime("%d/%m/%Y, %H:%M:%S")

        return iso_formatted
    except Exception as e:
        print(f"Erreur lors de la conversion de l'epoch en format ISO : {str(e)}")
        return None


def signal_handler(sig, frame):
    if pzDiscord:
        pzDiscord.stop_bot()
        print("Bot stopped.")
    exit(0)


@app.on_event("startup")
async def startup_db_client():
    print("startup")
    asyncio.create_task(start_bot())
    asyncio.create_task(monitor_process())
    asyncio.create_task(monitor_mod_update())


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

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
