from libs.Config import init_config
from fastapi import FastAPI
from routes import auth, console

CONF_FILE = "config.yml"
app_config = init_config(CONF_FILE)
app = FastAPI()
app.include_router(auth.router)
app.include_router(console.router)
