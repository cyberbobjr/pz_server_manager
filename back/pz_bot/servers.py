from discord.ext import commands

from libs.DatetimeHelper import DatetimeHelper
from libs.PZProcess import PZProcess


class ServerHandler(commands.Cog):
    def __init__(self, bot, exePath, authorized_channels):
        self.exePath = exePath
        self.authorized_channels = authorized_channels
        self.bot = bot
        self.pzProcess = PZProcess(exePath)
        return

    @commands.command()
    async def reboot(self, ctx, arg: str = None):
        if ctx.channel.id not in self.authorized_channels:
            return
        running_time = self.pzProcess.get_running_time()
        if running_time is None:
            msg = f'Le serveur n\'est pas démarré'
        else:
            msg = f':computer: Dernier reboot du serveur : {DatetimeHelper.epoch_to_iso(running_time)}'

        if msg is not None and self.bot.channel is not None:
            await ctx.send(msg)
