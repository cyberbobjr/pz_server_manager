from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from pz_setup import app_config

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
def get_config():
    return filter_sensitive_info(app_config.copy(), [
        "rcon.password",
        "ssh.password",
        "discord.apikey",
        "steam.apikey",
        "pz.password",
        "auth.secret",
        "auth.password"
    ])
