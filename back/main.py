import asyncio
import logging
import os
import signal

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from libs.security import decode_jwt
from pz_monitor import start_bot, monitor_mod_update, signal_handler
from pz_setup import pzDiscord, pzMonitoring
from routes import auth, mods, server, config

angular_static_path = os.path.join(os.path.dirname(__file__), 'front')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    print("Startup: FastAPI application is starting...")
    if pzDiscord:
        asyncio.create_task(start_bot())
        while not pzDiscord.is_ready:
            await asyncio.sleep(10)
    if pzMonitoring:
        asyncio.create_task(monitor_mod_update())


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(auth.router, prefix="/api")
app.include_router(server.router, prefix="/api", dependencies=[Depends(decode_jwt)])
app.include_router(mods.router, prefix="/api", dependencies=[Depends(decode_jwt)])
app.include_router(config.router, prefix="/api", dependencies=[Depends(decode_jwt)])

app.mount("/", StaticFiles(directory=angular_static_path, html=True), name="static")
