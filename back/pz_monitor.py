import asyncio
import logging
import signal

from libs.DatetimeHelper import DatetimeHelper
from libs.PZLog import PZLog
from pz_setup import pzGame, steam, pzRcon

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
                        logging.info(msg)
                        msg = f'servermsg The server will reboot in 5 minutes for updating mods...'
                        logging.info(msg)
                        await pzRcon.send_command(f"servermsg \"{msg}\"")
                        await asyncio.sleep(60 * 4)
                        msg = f'servermsg The server will reboot in 1 minute for updating mods...'
                        logging.info(msg)
                        await pzRcon.send_command(f"servermsg \"{msg}\"")
                        await asyncio.sleep(60)
                        await pzGame.save_server()
                        await asyncio.sleep(30)
                        await pzGame.restart_server()
                        await asyncio.sleep(10)
                        break
                except Exception as e:
                    logging.error(f'Error checking mod update for {workshop_id}: {e}')
                    continue
        await asyncio.sleep(30 * 60)  # Check every half-hour


def signal_handler(sig, frame):
    logging.info("Signal received, initiating graceful shutdown...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    logging.info("Cancelled ongoing tasks. Exiting.")
    asyncio.get_event_loop().stop()


def main():
    # Configure signal handling
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the monitor task
    logging.info("Startup: Launching mods monitor...")
    asyncio.run(monitor_mod_update())


if __name__ == "__main__":
    main()
