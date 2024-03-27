import asyncio
import os
import shutil
import signal

import yaml
from fastapi import APIRouter, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def filter_sensitive_info(config, sensitive_keys):
    for key in sensitive_keys:
        keys = key.split('.')
        target = config
        for k in keys[:-1]:
            if k in target:
                target = target[k]
            else:
                # Si une clé intermédiaire n'existe pas, sortez de la boucle pour éviter une KeyError
                break
        # Vérifiez si la dernière clé existe avant de tenter de la supprimer pour éviter KeyError
        if keys[-1] in target:
            target.pop(keys[-1], None)
    return config  # Retourne le dictionnaire modifié


@router.get("/config", tags=["config"])
async def read_config():
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yml')
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="config.yml not found")


@router.post("/config", tags=["config"])
async def update_config(new_config: dict = Body(...)):
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yml')
    backup_path = os.path.join(os.path.dirname(config_path),
                               f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml")

    # Copie du fichier actuel avant mise à jour
    try:
        shutil.copyfile(config_path, backup_path)
    except IOError as e:
        raise HTTPException(status_code=500, detail=f"Failed to backup config.yml: {e}")

    # Mise à jour du fichier config.yml avec les nouvelles données
    try:
        with open(config_path, 'w') as file:
            yaml.dump(new_config, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update config.yml: {e}")

    # Arrêter le script de manière propre après avoir retourné la réponse
    response = {"success": True, "msg": "Configuration updated successfully. Server is stopping for restart."}

    def stop_server():
        os.kill(os.getpid(), signal.SIGINT)

    # Utilisation d'un délai pour s'assurer que la réponse est envoyée avant l'arrêt
    asyncio.get_event_loop().call_later(1, stop_server)

    return response
