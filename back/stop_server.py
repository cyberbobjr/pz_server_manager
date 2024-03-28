import yaml

from libs.console import Console

# Chemin vers votre fichier config.yml
CONFIG_FILE_PATH = 'config.yml'


def load_rcon_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        return config['rcon']['host'], int(config['rcon']['port']), config['rcon']['password']


def stop_project_zomboid_server():
    try:
        host, port, password = load_rcon_config(CONFIG_FILE_PATH)
        rcon = Console((host, port), password)
        response = rcon.command("quit")
        response.close()
        print("Réponse RCON:", response)
    except Exception as e:
        print("Erreur lors de la tentative de stopper le serveur via RCON:", e)


if __name__ == "__main__":
    stop_project_zomboid_server()
