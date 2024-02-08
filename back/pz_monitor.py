import asyncio
import time

from libs.DatetimeHelper import DatetimeHelper
from libs.PZLog import PZLog
from pz_setup import pzDiscord, pzGame, steam


async def start_bot():
    await pzDiscord.run()


async def monitor_process():
    while True:
        is_process_running = pzGame.is_process_running()
        should_be_always_start = pzGame.should_be_always_start()
        if not is_process_running and should_be_always_start:
            await PZLog.print("Start server")
            await pzGame.start_server()
        await asyncio.sleep(60 * 2)  # check every 2 minutes


async def monitor_mod_update():
    while True:
        [_, workshop_ids] = pzGame.scan_mods_in_ini()
        running_time = pzGame.get_process_running_time()
        if running_time is not None:
            msg = f'Server running since {DatetimeHelper.epoch_to_iso(running_time)}'
            await PZLog.print(msg)
            for workshop_id in workshop_ids:
                last_update = steam.get_lastupdate_mod(workshop_id)
                if last_update > running_time:
                    msg = f'workshop item {workshop_id} was updated {DatetimeHelper.epoch_to_iso(last_update)} since {DatetimeHelper.epoch_to_iso(running_time)}, server rebooting'
                    await PZLog.print(msg)
                    await pzGame.stop_server()
                    while pzGame.is_process_running():
                        time.sleep(5)
                    await pzGame.start_server()
                    break
        await asyncio.sleep(60 * 60)  # check every hour


def signal_handler(sig, frame):
    if pzDiscord:
        pzDiscord.stop_bot()
        print("Bot stopped.")
    exit(-1)
