import tracemalloc
tracemalloc.start()
import asyncio
from pyrogram import Client
from config import load_config
from handlers import register_handlers
from database import init_database
from utils.logging import setup_logger
from browser.fetch_videos import init_session, close_session

async def main():
    config = load_config()
    logger = setup_logger()

    app = Client(
        "terabox_downloader",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN
    )

    try:
        await init_database()
        await init_session(max_concurrent_downloads=5)
        register_handlers(app)

        await app.start()
        logger.info("Bot started successfully")
        await asyncio.Future()  # This replaces idle()
    except Exception as e:
        logger.error(f"Error in main function: {e}")
    finally:
        await app.stop()
        await close_session()

if __name__ == "__main__":
    asyncio.run(main())