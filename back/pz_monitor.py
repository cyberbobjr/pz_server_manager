import asyncio
import logging
import signal

from libs.DatetimeHelper import DatetimeHelper
from libs.PZLog import PZLog
from pz_setup import pzGame, steam, pzRcon

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
ongoing_tasks = []


def signal_handler(sig, frame):
    logging.info("Signal received, initiating graceful shutdown...")
    for task in ongoing_tasks:
        task.cancel()
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*ongoing_tasks))
    logging.info("All tasks completed, exiting.")
    exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


async def monitor_mod_update():
    while True:
        [_, workshop_ids] = pzGame.scan_mods_in_ini()
        running_time = pzGame.get_process_running_time()
        if running_time is not None:
            for workshop_id in workshop_ids:
                try:
                    last_update = steam.get_lastupdate_mod(workshop_id)
                    if last_update is not None and last_update > running_time:
                        msg = f'workshop item {workshop_id} was updated {DatetimeHelper.epoch_to_iso(last_update)} since {DatetimeHelper.epoch_to_iso(running_time)}, server rebooting'
                        await PZLog.print(msg)
                        msg = f'servermsg The server will reboot in 5 minutes for updating mods...'
                        await PZLog.print(msg)
                        await pzRcon.send_command(f"servermsg \"{msg}\"")
                        await asyncio.sleep(60 * 4)
                        msg = f'servermsg The server will reboot in 1 minute for updating mods...'
                        await PZLog.print(msg)
                        await pzRcon.send_command(f"servermsg \"{msg}\"")
                        await asyncio.sleep(60)
                        await pzGame.stop_server()
                        break
                except Exception as e:
                    print(f'{e}')
                    continue
        await asyncio.sleep(30 * 60)  # check every demihour


if __name__ == "__main__":
    print("Startup: Launching mods monitor...")
    task = asyncio.create_task(monitor_mod_update())
    ongoing_tasks.append(task)
