from dotenv import load_dotenv
from os import getenv

load_dotenv()

DISCORD_TOKEN = getenv('DISCORD_TOKEN')
NOTICE_ROLE_ID = int(getenv('NOTICE_ROLE_ID'))
NOTICE_CHANNEL_ID = int(getenv('NOTICE_CHANNEL_ID'))
