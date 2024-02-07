import discord


class PZDiscord:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        intents = discord.Intents.default()
        # intents.messages = True
        self.client = discord.Client(intents=intents)

    async def send_message(self, message):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(self.channel_id)
        if channel:
            await channel.send(message)
        else:
            print("Channel not found.")

    async def start(self):
        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user}')

        await self.client.start(self.token)

    def stop_bot(self):
        print("Stopping bot...")
        self.client.close()

    async def run(self):
        await self.start()
