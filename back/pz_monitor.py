import asyncio
import time

from libs.DatetimeHelper import DatetimeHelper
from libs.PZLog import PZLog
from pz_setup import pzGame, steam, pzRcon


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
                        await pzRcon.send_command(f"servermsg {msg}")
                        time.sleep(60 * 4)
                        msg = f'servermsg The server will reboot in 1 minute for updating mods...'
                        await PZLog.print(msg)
                        await pzRcon.send_command(f"servermsg {msg}")
                        time.sleep(60)
                        await pzGame.stop_server()
                        break
                except Exception as e:
                    print(f'{e}')
                    continue
        await asyncio.sleep(30 * 60)  # check every demihour


def signal_handler(sig, frame):
    exit(-1)
