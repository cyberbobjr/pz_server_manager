import asyncio
import glob
import os
import subprocess

from .Bootstrap import Bootstrap
from .Mod import Mod
from .PZConfigFile import PZConfigFile
from .PZLog import PZLog
from .PZProcess import PZProcess

MODINFO = "mod.info"


class PZGame:
    mods: list[Mod] = []
    mod_path = "\\steamapps\\workshop\\content\\108600\\"
    memory = 8
    server_path = ""
    pz_exe_path = ""
    server_name = "servertest"
    pz_config: PZConfigFile
    pz_process: PZProcess
    pz_rcon = None

    def __init__(self, pz_exe_path: str, server_path: str, server_admin_password: str):
        self.must_restart = True
        self.server_admin_password = server_admin_password
        self.pz_exe_path = pz_exe_path
        self.server_path = server_path
        self.pz_config = PZConfigFile(self.server_path + '\\Zomboid\\Server\\' + self.server_name + '.ini')
        self.pz_process = PZProcess(self.pz_exe_path)

    def scan_mods_in_server_dir(self):
        self.mods = []
        for file in glob.glob(f'{self.pz_exe_path}{self.mod_path}*\\mods\\*\\{MODINFO}'):
            mod = self.parse_info(file)
            if mod is not None:
                self.mods.append(mod)

    def scan_mods_in_ini(self):
        mods = self.read_mods_ini()
        workshops = self.read_workshops_ini()
        return [mods, workshops]

    def read_mods_ini(self):
        return self.pz_config.get_value("Mods").split(";")

    def read_workshops_ini(self):
        return self.pz_config.get_value("WorkshopItems").split(";")

    def parse_info(self, file) -> Mod:
        workshop_id = None
        name = None
        mod_id = None
        pz_mod_path = f'{self.pz_exe_path}{self.mod_path}'
        with open(file) as f:
            try:
                for line in f:
                    if line.startswith("name"):
                        workshop_id = file[len(pz_mod_path):].split(os.path.sep)[0]
                        name = line.split("=")[1].strip()
                    if line.startswith("id"):
                        mod_id = line.split("=")[1].strip()
                if workshop_id is not None and name is not None and mod_id is not None:
                    mod = Mod(workshop_id, name, file)
                    mod.id = mod_id
                    return mod
            except:
                print(f"Error reading file {file}")

    def display_mods_infos(self):
        for mod in self.mods:
            print(mod)

    def build_server_mods_ini(self, Mods, WorkshopItems):
        self.set_server_ini("Mods", ';'.join(Mods) + "\n")
        self.set_server_ini("WorkshopItems", ';'.join(WorkshopItems) + "\n")

    def set_server_ini(self, key: str, value):
        return self.pz_config.write_value(key, value)

    def save_server_ini(self, content: str):
        return self.pz_config.put_content(content)

    def get_server_init(self, key=None):
        if key is None:
            return self.pz_config.get_content()
        return self.pz_config.get_value(key)

    def set_sandbox_options(self, sandbox_content):
        sandbox_path = f'{self.server_path}\\Zomboid\\Server\\{self.server_name}_SandboxVars.lua'
        with open(sandbox_path, 'w') as file:
            file.write(sandbox_content)
        return sandbox_content

    def get_sandbox_options(self):
        sandbox_path = f'{self.server_path}\\Zomboid\\Server\\{self.server_name}_SandboxVars.lua'
        with open(sandbox_path, 'r') as file:
            return file.read()

    def is_process_running(self) -> bool:
        return self.get_pid() is not None

    def get_pid(self):
        return self.pz_process.get_pid()

    def get_process(self):
        return self.pz_process.get_process()

    def get_process_running_time(self):
        return self.pz_process.get_running_time()

    async def start_server(self):
        from main import app_config
        if "log_filename" not in app_config["pz"]:
            app_config["pz"]["log_filename"] = "output.txt"
        java_command = f'"{self.get_exe_path()}\\jre64\\bin\\java.exe"'
        java_options = f'-Djava.awt.headless=true -Dzomboid.steam=1 -Dzomboid.znetlog=1 -XX:+UseZGC -XX:-CreateCoredumpOnCrash -XX:-OmitStackTraceInFastThrow -Xms{self.memory}g -Xmx{self.memory}g -Djava.library.path=natives/;natives/win64/;. -Duser.home="{self.server_path}" '
        classpath = f'-cp java/istack-commons-runtime.jar;java/jassimp.jar;java/javacord-2.0.17-shaded.jar;java/javax.activation-api.jar;java/jaxb-api.jar;java/jaxb-runtime.jar;java/lwjgl.jar;java/lwjgl-natives-windows.jar;java/lwjgl-glfw.jar;java/lwjgl-glfw-natives-windows.jar;java/lwjgl-jemalloc.jar;java/lwjgl-jemalloc-natives-windows.jar;java/lwjgl-opengl.jar;java/lwjgl-opengl-natives-windows.jar;java/lwjgl_util.jar;java/sqlite-jdbc-3.27.2.1.jar;java/trove-3.0.3.jar;java/uncommons-maths-1.2.3.jar;java/commons-compress-1.18.jar;java/'
        main_class = 'zombie.network.GameServer'
        additional_args = f'-statistic 0 -adminpassword {self.server_admin_password}'

        command = f'{java_command} {java_options} {classpath} {main_class} {additional_args}'
        await PZLog.print(f'Server is starting...')
        process = subprocess.Popen(command,
                                   creationflags=subprocess.CREATE_NEW_CONSOLE,
                                   cwd=self.get_exe_path())
        asyncio.create_task(self.check_when_server_ready())
        return process

    async def check_when_server_ready(self):
        while not Bootstrap.is_pzserver_ready(self, self.pz_rcon):
            await asyncio.sleep(10)
        await PZLog.print(f"Server is ready")

    async def stop_server(self):
        await PZLog.print(f'Server stopped')
        return await self.pz_rcon.send_command("quit")

    def should_be_always_start(self):
        return self.must_restart

    def set_be_always_start(self, state: bool):
        self.must_restart = state

    def get_exe_path(self) -> str:
        return f'{self.pz_exe_path}'

    def get_mod_path(self) -> str:
        return f'{self.pz_exe_path}{self.mod_path}'
