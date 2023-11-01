#Github.com/Vasusen-code

from pyrogram import Client
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from decouple import config
import logging, time, sys

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)

FORCESUB = config("FORCESUB", default=None)
AUTH = config("AUTH", default=None, cast=int)

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 
with Client("pyrogram" ,api_id=API_ID ,api_hash=API_HASH, hide_password=False) as userbot:
    SESSION = userbot.export_session_string()
    print("\n正在生成你的pyrogramSESSION...\n")
    print(SESSION)

Bot = Client("SaveRestricted",bot_token=BOT_TOKEN,api_id=int(API_ID),api_hash=API_HAS)    

try:
    Bot.start()
except Exception as e:
    print(error)
    sys.exit(1)
