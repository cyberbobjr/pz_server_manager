import time

import discord


class PZDiscord:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        intents = discord.Intents.default()
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
            print(f'Logged in as {self.client.user}')
            self.is_ready = True

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            if message.content.startswith('!players'):
                await self.handle_message(message)

        await self.client.start(self.token)

    async def handle_message(self, message):
        await message.channel.send(
            'Il y a actuellement X joueurs en ligne.')  # Remplacer X par le nombre réel de joueurs en ligne

    def stop_bot(self):
        print("Stopping bot...")
        self.client.close()

    async def run(self):
        await self.start()
