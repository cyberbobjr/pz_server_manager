import glob
import os
from libs.Mod import Mod

MODINFO = "mod.info"


class PZGame:
    mods: list[Mod] = []
    recipes = {}
    gamepath = ""

    def __init__(self, gamepath: str):
        self.init(gamepath)

    def init(self, gamepath: str):
        self.gamepath = gamepath

    def scan_mods(self):
        self.mods = []
        for file in glob.glob(self.gamepath + '/*/mods/*/' + MODINFO):
            mod = self.parse_info(file, self.gamepath)
            if mod is not None:
                self.mods.append(mod)

    def parse_info(self, file, gamepath) -> Mod:
        workshop_id = None
        name = None
        modId = None
        with open(file) as f:
            try:
                for line in f:
                    if line.startswith("name"):
                        workshop_id = file[len(gamepath):].split(os.path.sep)[1]
                        name = line.split("=")[1].strip()
                    if line.startswith("id"):
                        modId = line.split("=")[1].strip()
                if workshop_id is not None and name is not None and modId is not None:
                    mod = Mod(workshop_id, name, file)
                    mod.id = modId
                    return mod
            except:
                print(f"Error reading file {file}")

    def seek_recipes(self):
        for mod in self.mods:
            for recipe in mod.recipes.values():
                if recipe.result is not None:
                    result_name = recipe.result
                    if result_name in self.recipes.keys():
                        self.recipes[result_name].append(recipe)
                    else:
                        self.recipes[result_name] = [recipe]

    def display_mods_infos(self):
        for mod in self.mods:
            print(mod)

    def buildServerTestFile(self):
        WorkshopItems = []
        modIds = []
        f = open("server.ini", "w")
        for mod in self.mods:
            WorkshopItems.append(mod.workshopId)
            modIds.append(mod.id)
        f.write("WorkshopItems=" + ";".join(WorkshopItems) + "\n")
        f.write("Mods=" + ";".join(modIds))
        f.close()

    def exportAllMods(self):
        f = open("mods.txt", "w")
        for mod in self.mods:
            f.write(f"{mod.name}\n")
        f.close()
