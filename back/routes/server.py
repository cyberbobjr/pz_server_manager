import asyncio
import os
import signal
import subprocess

import psutil
from fastapi import Body, APIRouter

from mcrcon import MCRcon
from libs import Config
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
global process, output_process, output_error


@router.post("/server/command", tags=["server"])
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


@router.get("/server/status", tags=["server"])
async def status():
    from main import pzGame, pzRcon
    return {
        "process_running": pzGame.check_process(),
        "server_started": pzRcon.check_open()
    }


@router.get("/server/webconsole", tags=["server"])
async def webconsole():
    global process, output_process, output_error
    from main import pzGame
    if pzGame.check_process():
        output = await process.stdout.readline()
        if output:
            return output
    else:
        return {
            "success": False,
            "msg": "Server not started"
        }


@router.get("/server/start", tags=["server"])
async def start():
    from main import pzGame
    if pzGame.check_process():
        return {
            "success": False,
            "msg": "Server already started"
        }
    from main import app_config
    try:
        process_path = f'{app_config["pz"]["pz_exe_path"]}\\StartServer64.bat'
        global process
        process = await asyncio.create_subprocess_shell(
            cmd=process_path,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            shell=True,
            stdout=subprocess.PIPE)
        # TODO : remplir un log de façon continue
        return_code = process.returncode
        if return_code == 0:
            return {
                "success": True
            }
        else:
            return {
                "success": True,
                "msg": "The process was launched."
            }
    except Exception as e:
        print(f"An error occurred while executing the process: {str(e)}")
        return {
            "success": False,
            "msg": f"An error occurred while executing the process: {str(e)}"
        }


@router.get("/server/forcestop", tags=["server"])
async def force_stop():
    from main import pzGame
    if pzGame.check_process():
        try:
            pid = pzGame.get_pid()
            os.kill(pid, signal.SIGTERM)
            print("Process with PID", pid, "has been successfully stopped.")
            return {
                "success": True,
                "msg": f'Process with PID {pid} has been successfully stopped.'
            }
        except OSError as e:
            print("Unable to stop process with PID")
            return {
                "success": False,
                "msg": f'Unable to stop process with PID'
            }
