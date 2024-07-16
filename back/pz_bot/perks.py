from datetime import datetime, timedelta
from discord.ext import tasks, commands
from file_read_backwards import FileReadBackwards
import glob
import os
import re
import random


class PerkHandler(commands.Cog):
    """Class which handles the Perk log files"""

    def __init__(self, bot, logPath, authorized_channels):
        self.lastMessageTime = {}
        self.bot = bot
        self.authorized_channels = authorized_channels
        self.logPath = logPath
        self.lastUpdateTimestamp = datetime.now()
        self.loadHistory()
        self.update.start()
        self.notifyJoin = os.getenv("JOINS", "True") == "True"
        self.notifyDeath = os.getenv("DEATHS", "True") == "True"
        self.notifyPerk = os.getenv("PERKS", "True") == "True"
        self.notifyCreateChar = os.getenv("CREATECHAR", "True") == "True"

    def splitLine(self, line: str):
        """Split a log line into a timestamp and the remaining message"""
        timestampStr, message = line.strip()[1:].split("]", 1)
        timestamp = datetime.strptime(timestampStr, "%d-%m-%y %H:%M:%S.%f")
        return timestamp, message

    @tasks.loop(seconds=2)
    async def update(self):
        files = glob.glob(self.logPath + "/*PerkLog.txt")
        if len(files) > 0:
            with FileReadBackwards(files[0]) as f:
                newTimestamp = self.lastUpdateTimestamp
                for line in f:
                    timestamp, message = self.splitLine(line)
                    if timestamp > newTimestamp:
                        newTimestamp = timestamp
                    if timestamp > self.lastUpdateTimestamp:
                        message = self.handleLog(timestamp, message, fromUpdate=True)
                        if message is not None and self.bot.channel is not None:
                            await self.bot.channel.send(message)
                    else:
                        break
                self.lastUpdateTimestamp = newTimestamp

    # Load the history from the files up until the last update time
    def loadHistory(self):
        self.bot.log.info("Loading Perk history...")

        # Go through each user file in the log folder and subfolders
        print(self.logPath)
        files = glob.glob(self.logPath + "/**/*PerkLog.txt", recursive=True)
        files.sort(key=os.path.getmtime)
        for file in files:
            with open(file) as f:
                for line in f:
                    self.handleLog(*self.splitLine(line))
        self.bot.log.info("Perk history loaded")

    # Parse a line in the user log file and take appropriate action

    def handleLog(self, timestamp: datetime, message: str, fromUpdate=False):
        # Ignore the id at the start of the message, no idea what it's for
        message = message[message.find("[", 2) + 1:]

        # Next is the name which we use to get the user
        name, message = message.split("]", 1)
        userHandler = self.bot.get_cog("UserHandler")
        user = userHandler.getUser(name)
        char_name = userHandler.getCharName(name) if fromUpdate and user else None
        log_char_string = 'aka ' + char_name + ' ' if char_name else ''

        # Then position which we set if it's more recent
        x = message[1: message.find(",")]
        y = message[message.find(",") + 1: message.find(",", message.find(",") + 1)]
        message = message[message.find("[", 2) + 1:]

        if timestamp > user.lastSeen:
            user.lastSeen = timestamp
            user.lastLocation = (x, y)

        # Then the message type, can be "Died", "Login", "Level Changed" or a list of perks
        type, message = message.split("]", 1)

        # All these logs should include hours survived
        match = re.search(r"Hours Survived: (\d+)", message)
        if match:
            hours = match.group(1)
        else:
            hours = '0'  # Ou une autre valeur par défaut appropriée
        user.hoursAlive = hours
        if int(hours) > int(user.recordHoursAlive):
            user.recordHoursAlive = hours

        cooldown_period = timedelta(seconds=30)  # Définissez votre période de cooldown
        now = datetime.now()
        if user.name in self.lastMessageTime and now - self.lastMessageTime[user.name] < cooldown_period:
            return None  # Sortez de la fonction si le dernier message est trop récent

        if type == "Died":
            user.died.append(timestamp)
            if timestamp > self.lastUpdateTimestamp:
                self.bot.log.info(f"{user.name} died")
                if self.notifyDeath:
                    return self.get_death_message(user.name, log_char_string, int(user.hoursAlive))
        elif type == "Login":
            if timestamp > self.lastUpdateTimestamp:
                user.online = True
                self.bot.log.info(f"{user.name} login")
                if self.notifyJoin:
                    return self.get_welcome_message(user.name, log_char_string, int(user.hoursAlive))
        elif "Created Player" in type:
            if timestamp > self.lastUpdateTimestamp:
                user.online = True
                self.bot.log.info(f"{user.name} new character")
                if self.notifyCreateChar:
                    return f":person_raising_hand: {user.name} {log_char_string}se réveille en pleine apocalypse..."
        elif type == "Level Changed":
            match = re.search(r"\[(\w+)\]\[(\d+)\]", message)
            perk = match.group(1)
            level = match.group(2)
            user.perks[perk] = level
            if timestamp > self.lastUpdateTimestamp:
                self.bot.log.info(f"{user.name} {perk} changed to {level}")
                if self.notifyPerk:
                    return self.get_level_up_message(user.name, perk, int(level), log_char_string)
        else:
            # Must be a list of perks following a login/player creation
            for (name, value) in re.findall(r"(\w+)=(\d+)", type):
                user.perks[name] = value

    def get_death_message(self, user_name, log_char_string, hoursAlive):
        if hoursAlive < 10:
            messages = [
                f":skull: {user_name} {log_char_string}a rejoint les morts-vivants après seulement {hoursAlive} heure(s). La dure loi de l'apocalypse.",
                f":ghost: {user_name} {log_char_string}est tombé au combat! {hoursAlive} heure(s) de survie, mais chaque seconde compte.",
                f":zombie: À peine le temps de découvrir le monde, {user_name} {log_char_string}est déjà un souvenir, après {hoursAlive} heure(s) de lutte.",
                f":coffin: Fin tragique pour {user_name} {log_char_string}qui a survécu {hoursAlive} heure(s). Repose en paix, brave âme."
            ]
        elif hoursAlive < 100:
            messages = [
                f":broken_heart: {user_name} {log_char_string}nous a quittés après {hoursAlive} courageuses heures. Une perte déchirante.",
                f":sob: Le monde est un peu plus sombre sans {user_name} {log_char_string}et ses {hoursAlive} heures de survie.",
                f":boom: {user_name} {log_char_string}a explosé en héros, avec {hoursAlive} heures au compteur. Quelle fin spectaculaire!",
                f":cry: C'est la fin de l'aventure pour {user_name} {log_char_string}après {hoursAlive} heures. Trop tôt pour dire au revoir."
            ]
        elif hoursAlive < 500:
            messages = [
                f":clap: {user_name} {log_char_string}a fait un voyage impressionnant, survivant {hoursAlive} heures. Applaudissements éternels.",
                f":star_struck: {user_name} {log_char_string}, une légende après {hoursAlive} heures, s'est éteinte. Son étoile brille toujours.",
                f":thunder_cloud_and_rain: Après la tempête de {hoursAlive} heures, {user_name} {log_char_string}trouve le repos. Une fin mémorable."
            ]
        else:  # 500 heures et plus
            messages = [
                f":crown: {user_name} {log_char_string}, avec plus de {hoursAlive} heures de survie, a finalement rejoint le panthéon des héros.",
                f":sparkles: Une épopée s'achève. {user_name} {log_char_string}, après {hoursAlive} heures, laisse un héritage inoubliable.",
                f":dizzy: La légende de {user_name} {log_char_string}, qui a survécu {hoursAlive} heures, continuera d'inspirer.",
                f":fireworks: {user_name} {log_char_string}a survécu {hoursAlive} heures. Quelle vie! Célébrons cette aventure extraordinaire."
            ]

        # Choose a random message from the appropriate list
        return random.choice(messages)

    def get_welcome_message(self, user_name, log_char_string, hoursAlive):
        if hoursAlive == 0:
            messages = [
                f":hatching_chick: {user_name} {log_char_string}vient d'entrer dans le monde apocalyptique. Bienvenue dans la zone de survie!",
                f":baby: Nouveau survivant détecté! {user_name} {log_char_string}se prépare pour ses premières heures de survie.",
                f":sparkles: {user_name} {log_char_string}est fraîchement débarqué(e)! Prépare-toi à affronter les hordes!",
                f":seedling: Bienvenue à {user_name} {log_char_string}qui fait ses premiers pas dans cet univers impitoyable.",
                f":new: {user_name} {log_char_string}a rejoint la résistance! Le début d'une longue aventure."
            ]
        elif hoursAlive < 500:
            messages = [
                f":runner: {user_name} {log_char_string}est de retour, avec {hoursAlive} heure(s) de survie au compteur. On progresse!",
                f":muscle: {user_name} {log_char_string}continue son aventure, fort de {hoursAlive} heure(s) d'expérience.",
                f":wrench: Après {hoursAlive} heure(s) de survie, {user_name} {log_char_string}est prêt(e) pour plus d'action!",
                f":camping: {user_name} {log_char_string}a survécu {hoursAlive} heure(s). Quelle sera la prochaine étape?",
                f":walking: {user_name} {log_char_string}a brisé le silence, {hoursAlive} heure(s) après avoir commencé. Continuons ainsi!"
            ]
        elif hoursAlive > 1000:  # Plus de 1000 heures de survie
            messages = [
                f":star2: {user_name} {log_char_string}est un maître de la survie avec plus de 1000 heures au compteur! Respect.",
                f":fire: {user_name} {log_char_string}a dépassé les 1000 heures de survie! Un véritable phénix parmi nous.",
                f":comet: Avec plus de 1000 heures de survie, {user_name} {log_char_string}brille plus fort que jamais dans le ciel apocalyptique.",
                f":wizard: {user_name} {log_char_string}est un sorcier de la survie! Plus de 1000 heures d'expériences et de secrets à partager.",
                f":alien: {user_name} {log_char_string}a exploré des territoires que peu ont vu, survivant plus de 1000 heures. Légendaire!"
            ]
        else:  # 500 heures et plus
            messages = [
                f":crown: Une légende revient parmi nous! {user_name} {log_char_string}avec plus de 500 heures de survie à son actif.",
                f":sunglasses: {user_name} {log_char_string}est un véritable vétéran, ayant survécu plus de 500 heures. Chapeau bas!",
                f":shield: Attention, {user_name} {log_char_string}est là. Avec plus de 500 heures de survie, c'est un pilier de la communauté.",
                f":crossed_swords: {user_name} {log_char_string}le survivant légendaire est de retour, prêt à ajouter plus d'heures à son palmarès!",
                f":trophy: {user_name} {log_char_string}a franchi le cap des 500 heures! Un exploit à célébrer."
            ]

        # Choose a random message from the appropriate list
        return random.choice(messages)

    def get_level_up_message(self, user_name, perk, level, log_char_string):
        if level == 1:
            messages = [
                f":star2: Incroyable, {user_name} {log_char_string}a débuté son voyage en {perk}, atteignant le niveau {level}!",
                f":baby: {user_name} {log_char_string}fait ses premiers pas en {perk}! Niveau {level} atteint, que l'aventure commence.",
                f":hatching_chick: {user_name} {log_char_string}éclot en {perk}! Niveau {level} déjà en poche.",
            ]
        elif level < 5:
            messages = [
                f":muscle: {user_name} {log_char_string}gagne en puissance en {perk}, atteignant le niveau {level}!",
                f":man_running: Avec détermination, {user_name} {log_char_string}progresse en {perk} et atteint le niveau {level}.",
                f":hammer_and_wrench: {user_name} {log_char_string}construit ses compétences en {perk}, arrivant au niveau {level}.",
            ]
        elif level < 10:
            messages = [
                f":fire: {user_name} {log_char_string}est en feu! Niveau {level} atteint en {perk}. La maîtrise se rapproche.",
                f":rocket: {user_name} {log_char_string}décolle vers les étoiles en {perk}, atteignant fièrement le niveau {level}.",
                f":zap: Électrisant! {user_name} {log_char_string}frappe fort en {perk} avec le niveau {level} désormais atteint.",
            ]
        else:  # Niveau 10
            messages = [
                f":trophy: {user_name} {log_char_string}est un maître incontesté en {perk}, ayant atteint le niveau {level}! Félicitations!",
                f":crown: Royauté! {user_name} {log_char_string}domine le domaine de {perk}, parvenu au niveau {level}.",
                f":sparkles: {user_name} {log_char_string}brille de mille feux en {perk}, avec le niveau {level} atteint. La perfection.",
            ]

        # Choose a random message from the appropriate list
        return random.choice(messages)
