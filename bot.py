# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
# Clone Code Credit : YT - @Tech_VJ / TG - @VJ_Bots / GitHub - @VJBots

import sys, glob, importlib, logging, logging.config, pytz, asyncio
from pathlib import Path

# Logging setup
logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

from pyrogram import Client, idle
from database.users_chats_db import db
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from Script import script
from datetime import date, datetime
from aiohttp import web
from plugins import web_server

from TechVJ.bot import TechVJBot
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

# Load all plugins
ppath = "plugins/*.py"
files = glob.glob(ppath)

# ✅ Start the main bot client
TechVJBot.start()

# ✅ Proper event loop initialization for Python 3.11+
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def start():
    print("\nInitalizing Your Bot")
    bot_info = await TechVJBot.get_me()
    await initialize_clients()

    # Import all plugin files
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = f"plugins.{plugin_name}"
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Tech VJ Imported => " + plugin_name)

    # Keepalive ping for Heroku or Koyeb
    if ON_HEROKU:
        asyncio.create_task(ping_server())

    print(f"Bot started successfully as @{bot_info.username}")

# ✅ Run the async start() and keep bot alive with idle()
if __name__ == "__main__":
    try:
        loop.run_until_complete(start())
        idle()  # <--- Keeps the bot running and responsive
    except KeyboardInterrupt:
        print("Bot stopped manually.")
