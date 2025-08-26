import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv("TOKEN"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
