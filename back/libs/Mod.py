import os
import pathlib
import re
import codecs
from libs.Recipe import Recipe

REGEX_IMPORTS = "\\s*imports(.*)\\s+\\{([^}]+)\\}"
REGEX_RECIPE = "\\s*recipe (.*)\\s+\\{([^}]+)\\}"
REGEX_MODULE = "\\s*module (.*)$"
EXT = ".txt"


class Mod:
    id = str

    def __init__(self, workshop_id, name, file):
        self.workshopId = workshop_id
        self.name = name
        self.path = os.path.dirname(file)
        self.file = file
        self.id = None
        self.recipes = {}

    def __str__(self):
        return f"{self.workshopId} / {self.id} => {self.name} ({self.path})"

    def seek_recipe(self):
        for file in pathlib.Path(self.path).rglob("*" + EXT):
            path = str(file)
            with codecs.open(path, 'r', encoding="utf-8", errors="ignore") as f:
                data = f.read()
                baseRegex = re.finditer(REGEX_IMPORTS, data, flags=re.IGNORECASE)
                base = "Base"
                if baseRegex is not None:
                    for matchNum, match in enumerate(baseRegex, start=1):
                        base = match.group(2).strip().replace(",", "")
                matches = re.finditer(REGEX_RECIPE, data, flags=re.IGNORECASE)
                if matches is not None:
                    for matchNum, match in enumerate(matches, start=1):
                        if len(match.groups()) > 2:
                            print("ERROR too many group for one recipe")
                            exit(1)
                        recipe_name = match.group(1).strip()
                        recipe = match.group(2).split("\r\n")
                        self.recipes[recipe_name] = Recipe(recipe_name, recipe, base, path)
