import logging
import os
import uvicorn

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from libs.security import decode_jwt
from pz_setup import app_config
from routes import auth, mods, server, config, modpacks

angular_static_path = os.path.join(os.path.dirname(__file__), 'front')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(auth.router, prefix="/api")
app.include_router(server.router, prefix="/api", dependencies=[Depends(decode_jwt)])
app.include_router(mods.router, prefix="/api", dependencies=[Depends(decode_jwt)])
app.include_router(config.router, prefix="/api", dependencies=[Depends(decode_jwt)])
app.include_router(modpacks.router, prefix="/api", dependencies=[Depends(decode_jwt)])

app.mount("/", StaticFiles(directory=angular_static_path, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app,
                host=app_config["server"]["host"],
                port=app_config["server"]["port"],
                ssl_keyfile=app_config["server"]["ssl_keyfile"],
                ssl_certfile=app_config["server"]["ssl_certfile"],
                )