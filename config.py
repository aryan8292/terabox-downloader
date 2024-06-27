import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.API_ID = os.getenv("API_ID")
        self.API_HASH = os.getenv("API_HASH")
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.DB_NAME = os.getenv("DB_NAME", "terabox_links.db")
        self.MAX_CONCURRENT_DOWNLOADS = int(os.getenv("MAX_CONCURRENT_DOWNLOADS", 5))
        self.BOT_USERNAME = os.getenv("bot_username")
        self.DUMMY_ID = os.getenv("dummy_id")

def load_config():
    return Config()