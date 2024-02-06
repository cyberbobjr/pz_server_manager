import os
import signal
import time
from typing import List

from fastapi import Body, APIRouter

from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/server/command", tags=["server"])
async def command(cmd: str = Body()):
    try:
        from main import pzGame, pzRcon
        result = await pzRcon.send_command(cmd)
        if result is False:
            return {
                "success": False,
                "msg": "Commande not sent"
            }
        return {
            "success": True,
            "msg": result
        }
    except Exception as e:
        print(e)


@router.get("/server/status", tags=["server"])
async def status():
    from main import pzGame, pzRcon
    return {
        "process_running": pzGame.is_process_running(),
        "server_started": pzRcon.check_open()
    }


@router.get("/server/webconsole", tags=["server"])
async def webconsole():
    from main import app_config, pzGame
    if "log_filename" not in app_config["pz"]:
        app_config["pz"]["log_filename"] = "output.txt"
    filepath = f'{pzGame.get_exe_path()}\\{app_config["pz"]["log_filename"]}'
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.readlines()
    else:
        return {
            "success": False,
            "msg": "Server not started"
        }


@router.get("/server/restart", tags=["server"])
async def restart():
    from main import pzGame
    if pzGame.is_process_running():
        await pzGame.stop_server()
        while pzGame.is_process_running():
            time.sleep(5)
        pz_process = pzGame.start_server()
        pzGame.set_be_always_start(True)
        return {
            "success": True,
            "msg": f'Server restarted with the pid {pz_process.pid}'
        }
    else:
        return {
            "success": False,
            "msg": f'Server not started'
        }


@router.get("/server/start", tags=["server"])
async def start():
    from main import pzGame
    if pzGame.is_process_running():
        return {
            "success": False,
            "msg": "Server already started"
        }
    try:
        pz_process = pzGame.start_server()
        pzGame.set_be_always_start(True)
        return_code = pz_process.returncode
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


@router.get("/server/stop", tags=["server"])
async def stop():
    try:
        from main import pzGame
        pzGame.stop_server()
        pzGame.set_be_always_start(False)
        return {
            "success": True,
            "msg": "Server stopped"
        }
    except Exception as e:
        return {
            "success": False,
            "msg": e
        }


@router.get("/server/forcestop", tags=["server"])
async def force_stop():
    from main import pzGame
    if pzGame.is_process_running():
        try:
            pid = pzGame.get_pid()
            os.kill(pid, signal.SIGTERM)
            print("Process with PID", pid, "has been successfully stopped.")
            pzGame.set_be_always_start(False)
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


@router.post("/server/mods", tags=["server"])
async def save_mods_ini(Mods: List[str], WorkshopItems: List[str]):
    try:
        from main import pzGame
        pzGame.build_server_mods_ini(Mods, WorkshopItems)
        return {
            "success": True,
            "msg": "ini file saved"
        }
    except Exception as e:
        return {
            "success": False,
            "msg": e
        }


@router.post("/server/settings", tags=["server"])
async def save_server_settings(key: str, value):
    try:
        from main import pzGame
        return {
            "success": True,
            "msg": pzGame.build_server_ini(key, value)
        }
    except Exception as e:
        return {
            "success": False,
            "msg": e
        }
