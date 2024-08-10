import subprocess
import os
import sys
import json
import time
import discord
from colorama import Fore, Style
from utils.cloner import Cloner
from utils.panel import Panel, Panel_Run
from discord import Client, Intents
from rich.prompt import Prompt, Confirm
from time import sleep

GREEN = Fore.GREEN + Style.BRIGHT

def rename_console(title):
    if os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")

rename_console("Discord Server Cloner")

try:
    client = Client(intents=Intents.all())
except Exception as e:
    print(f"{GREEN}> Unable to create Discord client: ", e)

with open("./utils/config.json", "r") as json_file:
    data = json.load(json_file)

os.system('cls' if os.name == 'nt' else 'clear')

def clear(option=False):
    sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    if option:
        user = client.user
        guild = client.get_guild(int(INPUT_GUILD_ID))
        Panel_Run(guild, user)
    else:
        Panel()

async def clone_server():
    start_time = time.time()
    guild_from = client.get_guild(int(INPUT_GUILD_ID))
    print(" ")
    guild_to = client.get_guild(int(GUILD))
    
    await Cloner.guild_create(guild_to, guild_from)
    
    await Cloner.channels_delete(guild_to)
    if data["copy_settings"]["roles"]:
        await Cloner.roles_create(guild_to, guild_from)
    if data["copy_settings"]["categories"]:
        await Cloner.categories_create(guild_to, guild_from)
    if data["copy_settings"]["channels"]:
        await Cloner.channels_create(guild_to, guild_from)
    if data["copy_settings"]["emojis"]:
        await Cloner.emojis_create(guild_to, guild_from)
    print(f"{GREEN}\n> Server cloned in " + str(round(time.time() - start_time, 2)) + " seconds")

@client.event
async def on_ready():
    clear(True)
    await clone_server()

class ClonerBot:
    def __init__(self):
        self.INPUT_GUILD_ID = None
        with open("./utils/config.json", "r") as json_file:
            self.data = json.load(json_file)

    def clear(self):
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        Panel()

    def edit_config(self, option, value, copy_settings=False):
        if copy_settings:
            self.data["copy_settings"][option] = value
        else:
            self.data[option] = value
        with open("./utils/config.json", "w") as json_file:
            json.dump(self.data, json_file, indent=4)

    def edit_settings_function(self):
        print(f"{GREEN}\nYou want to copy:")
        categories = Confirm.ask("> Categories?")
        channels = Confirm.ask("> Channels?")
        roles = Confirm.ask("> Roles?")
        emojis = Confirm.ask("> Emojis?")
        for option in ["categories", "channels", "roles", "emojis"]:
            self.edit_config(option, locals()[option], copy_settings=True)

    def main(self):
        self.clear()
        if self.data["token"] == False:
            self.TOKEN = Prompt.ask("\n> Enter your Token")
            sleep(0.5)
        else:
            print(f"{GREEN}> Token found")
        self.clear()
        edit_settings = Confirm.ask("\n> Do you want to edit the settings?")
        sleep(0.5)
        self.clear()
        if edit_settings:
            self.edit_settings_function()
        sleep(0.5)
        self.clear()

        self.INPUT_GUILD_ID = Prompt.ask("\n> Server to copy")
        sleep(0.5)
        self.clear()

        self.GUILD = Prompt.ask("\n> Server to paste")
        sleep(0.5)
        self.clear()

        return self.INPUT_GUILD_ID, self.TOKEN, self.GUILD

if __name__ == "__main__":
    INPUT_GUILD_ID, TOKEN, GUILD = ClonerBot().main()
    try:
        client.run(TOKEN, bot=False)
        clear()
    except Exception as e:
        print(e)
        print(f"{GREEN}> Invalid Token")
        data["token"] = False



