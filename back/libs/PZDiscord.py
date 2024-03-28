import re
import time
import discord

from libs.DatetimeHelper import DatetimeHelper


class PZDiscord:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.is_ready = False

    async def send_message(self, message):
        while not self.client.is_ready:
            time.sleep(10)
        channel = self.client.get_channel(self.channel_id)
        if channel:
            await channel.send(message)
        else:
            print("Channel not found.")

    async def start(self):
        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user.name}')
            self.is_ready = True

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            if message.content.startswith('!players'):
                await self.send_player_count(message)
            if message.content.startswith('!reboot'):
                await self.last_reboot(message)

        await self.client.start(self.token)

    async def send_player_count(self, message):
        player_count = await self.get_players()
        if player_count <= 1:
            await message.channel.send(f'Il y a actuellement {player_count} joueur en ligne.')
        else:
            await message.channel.send(f'Il y a actuellement {player_count} joueurs en ligne.')

    async def last_reboot(self, message):
        from pz_setup import pzGame
        running_time = pzGame.get_process_running_time()
        if running_time is None:
            msg = f'Le serveur n\'est pas démarré'
        else:
            msg = f'Dernier reboot du serveur : {DatetimeHelper.epoch_to_iso(running_time)}'
        await message.channel.send(msg)

    @staticmethod
    async def get_players():
        from pz_setup import pzRcon
        players = await pzRcon.send_command("players")
        regex = r"\((\d+)\)"
        match = re.search(regex, players)
        player_count = 0
        if match:
            player_count = int(match.group(1))
        return player_count

    def stop_bot(self):
        print("Stopping bot...")
        self.client.close()

    async def run(self):
        await self.start()
