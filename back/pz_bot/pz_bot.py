# The main file for zomboi bot. Sets up and runs the discord client

import logging
import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

from maps import MapHandler
from perks import PerkHandler
from users import UserHandler

chemin_repertoire_frere = Path(__file__).resolve().parent.parent
sys.path.append(str(chemin_repertoire_frere))

from libs.Config import init_config

CONF_FILE = Path(__file__).resolve().parent.parent / "config.yml"
app_config = init_config(CONF_FILE)
mapPath = os.path.join(app_config["pz"]["pz_exe_path"], "media", "maps")
savePath = os.path.join(app_config["pz"]["server_path"], "Zomboid", "db")

load_dotenv(override=True)

# Verify the log path
logPath = os.path.join(app_config["pz"]["server_path"], "Zomboid", "Logs")
print(f'Log path : {logPath}')

if logPath is None or len(logPath) == 0:
    logging.error("Zomboid log path not set and unable to find default")
    exit()

# Our main bot object
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
zomboi = commands.bot.Bot("!", intents=intents)

# Redirect the discord log to a file
logFormat = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
discordLogger = logging.getLogger("discord")
discordLogger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logFormat)
discordLogger.addHandler(handler)

# set up our logging
zomboi.log = logging.getLogger("zomboi")
handler = logging.StreamHandler()
handler.setFormatter(logFormat)
handler.setLevel(logging.INFO)
zomboi.log.addHandler(handler)
handler = logging.FileHandler(filename="zomboi.log")
handler.setFormatter(logFormat)
handler.setLevel(logging.DEBUG)
zomboi.log.addHandler(handler)
zomboi.log.setLevel(logging.DEBUG)


@zomboi.event
async def on_ready():
    zomboi.log.info(f"We have logged in as {zomboi.user}")
    channel = str(app_config["discord"]["channel"])
    zomboi.channel = zomboi.get_channel(int(channel)) if channel.isdigit() else None  # Find by id
    if zomboi.channel is None:
        zomboi.channel = discord.utils.get(
            zomboi.get_all_channels(), name=channel
        )  # find by name
    if zomboi.channel is None:
        zomboi.log.warning("Unable to get channel, will not be enabled")
    else:
        zomboi.log.info("channel connected")
    await zomboi.add_cog(UserHandler(zomboi, logPath, savePath))
    # await zomboi.add_cog(ChatHandler(zomboi, logPath))
    await zomboi.add_cog(PerkHandler(zomboi, logPath))
    # await zomboi.add_cog(RCONAdapter(zomboi))
    await zomboi.add_cog(MapHandler(zomboi, mapPath))
    # await zomboi.add_cog(AdminLogHandler(zomboi, logPath))


# Always finally run the bot
token = app_config["discord"]["apikey"]
if token is None:
    zomboi.log.error("DISCORD_TOKEN environment variable not found")
    exit()

zomboi.run(token)
