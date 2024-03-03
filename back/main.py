import asyncio
import signal

import uvicorn
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from libs.Bootstrap import Bootstrap
from libs.security import decode_jwt
from pz_monitor import start_bot, monitor_process, monitor_mod_update, signal_handler
from pz_setup import app_config, steamcmd, pzDiscord
from routes import auth, mods, server

if not Bootstrap.is_pzserver_installed(app_config["pz"]["pz_exe_path"]):
    Bootstrap.install_pzserver(app_config["pz"]["pz_exe_path"], steamcmd)
    '''
    Server not installed, so we install it, and we ask for relaunching the server, 
    that way the directory structure for server will be created
    '''
    print(f'Relaunch the server...')
    exit(0)

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    print("startup")
    if pzDiscord:
        asyncio.create_task(start_bot())
        while not pzDiscord.is_ready:
            await asyncio.sleep(10)
        asyncio.create_task(monitor_process())
        asyncio.create_task(monitor_mod_update())
    else:
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
app.include_router(server.router, dependencies=[Depends(decode_jwt)])
app.include_router(mods.router, dependencies=[Depends(decode_jwt)])
# app.mount("/static", StaticFiles(directory=os.path.abspath(modpack_path)), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host=app_config["server"]["host"], port=app_config["server"]["port"])
