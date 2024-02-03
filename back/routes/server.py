import os
import signal
import subprocess
from fastapi import Body, APIRouter

from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
global pz_process
output_file_name = "output.txt"


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
        "process_running": pzGame.check_process(),
        "server_started": pzRcon.check_open()
    }


@router.get("/server/webconsole", tags=["server"])
async def webconsole():
    global pz_process
    from main import pzGame
    from main import app_config
    filepath = f'{app_config["pz"]["pz_exe_path"]}\\{output_file_name}'
    if pzGame.check_process():
        with open(filepath, "r") as f:
            return f.readlines()
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
        process_path = f'{app_config["pz"]["pz_exe_path"]}\\StartServer64.bat > {output_file_name}'
        global pz_process, output_thread
        pz_process = subprocess.Popen(process_path,
                                      cwd=app_config["pz"]["pz_exe_path"],
                                      creationflags=subprocess.CREATE_NEW_CONSOLE)
        # TODO : remplir un log de façon continue
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
