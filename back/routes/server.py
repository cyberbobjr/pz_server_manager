import asyncio
import os
import signal
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Union

from fastapi import Body, APIRouter, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from pz_setup import pzRcon, pzGame, app_config, steamcmd, pzDiscord

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

task_status = {}


class FileContent(BaseModel):
    content: str
    type: str


@router.post("/server/command", tags=["server"])
async def command(cmd: str = Body()):
    try:
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
    return {
        "server_started": pzRcon.check_open(),
        "running_since": pzGame.get_process_running_time()
    }


@router.get("/server/webconsole", tags=["server"])
async def webconsole():
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
    if pzGame.is_process_running():
        return {
            "success": False,
            "msg": "Server already started"
        }
    try:
        pz_process = await pzGame.start_server()
        pzDiscord.send_message(f'Server is starting...')
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
        pzDiscord.send_message(f'Server is stopping...')
        if not await pzGame.stop_server():
            return {
                "success": False,
                "msg": "Server not responding"
            }
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
async def save_mods_ini(Mods: List[str], WorkshopItems: List[str], Maps: List[str], background_tasks: BackgroundTasks):
    try:
        appid = app_config["steam"]["appid"]
        exePath = pzGame.get_exe_path()

        for workshopItem in WorkshopItems:
            if not pzGame.is_workshop_exist_in_server_dir(workshopItem):
                # Ajouter la tâche d'installation en arrière-plan
                background_tasks.add_task(background_install_workshopfiles, appid, workshopItem, exePath)
            else:
                task_status[workshopItem] = "completed"

        pzGame.build_server_mods_ini(Mods, WorkshopItems, Maps)
        return {
            "success": True,
            "msg": "ini file saved"
        }
    except Exception as e:
        return {
            "success": False,
            "msg": str(e)
        }


def install_workshopfiles_async(appid: str, workshopItem: str, exePath: str):
    task_status[workshopItem] = "in progress"
    try:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(steamcmd.install_workshopfiles, appid, workshopItem, exePath)
            result = future.result()
            # Update the task status to "completed"
            task_status[workshopItem] = "completed"
            return result
    except Exception as e:
        # Update the status with the error in case of an exception
        task_status[workshopItem] = f"Error: {str(e)}"


async def background_install_workshopfiles(appid: str, workshopItem: str, exePath: str):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, install_workshopfiles_async, appid, workshopItem, exePath)


@router.get("/server/task/")
async def get_task_status_or_in_progress(workshopItem: str = None) -> Union[List[str], dict]:
    if workshopItem:
        return {"workshopItem": workshopItem, "status": task_status.get(workshopItem, "Not found")}
    else:
        in_progress_tasks = [item for item, status in task_status.items() if status == "in progress"]
        return in_progress_tasks


@router.put("/server/settings", tags=["server"])
async def save_server_settings(key: str, value):
    try:
        return {
            "success": True,
            "msg": pzGame.set_server_ini(key, value)
        }
    except Exception as e:
        return {
            "success": False,
            "msg": e
        }


@router.post("/server/config", tags=["server"])
async def save_server_settings(data: FileContent):
    try:
        return {
            "success": True,
            "msg": pzGame.save_content(data.type, data.content)
        }
    except Exception as e:
        return {
            "success": False,
            "msg": e
        }


@router.get("/server/config", tags=["server"])
async def get_server_settings(content_type: str):
    try:
        return {
            "success": True,
            "msg": pzGame.get_content(content_type)
        }
    except Exception as e:
        return {
            "success": False,
            "msg": e
        }
