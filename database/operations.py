import aiosqlite
from config import load_config
from utils.logging import get_logger

logger = get_logger(__name__)
config = load_config()

async def insert_terabox_links(user_id, file_type, sizes, original_caption, original_thumbnail, unique_string):
    async with aiosqlite.connect(config.DB_NAME) as db:
        try:
            cursor = await db.execute('''INSERT INTO terabox_links
                                (user_id, file_type, sizes, original_caption, original_thumbnail, unique_string)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                             (user_id, file_type, sizes, original_caption, original_thumbnail, unique_string))
            
            await db.commit()
            return cursor.lastrowid 
        except Exception as e:
            logger.error(f"Error inserting terabox link: {e}")
            raise

async def insert_video_info(user_id, reference_id, unique_str, argument):
    async with aiosqlite.connect(config.DB_NAME) as db:
        try:
            await db.execute('''INSERT INTO video_info
                                (user_id, reference_id, unique_str, argument)
                                VALUES (?, ?, ?, ?)''',
                             (user_id, reference_id, unique_str, argument))
            await db.commit()
        except Exception as e:
            logger.error(f"Error inserting video info: {e}")
            raise

async def retrieve_video_info(argument):
    async with aiosqlite.connect(config.DB_NAME) as db:
        try:
            async with db.execute("SELECT unique_str FROM video_info WHERE argument = ?", (argument,)) as cursor:
                result = await cursor.fetchone()
                return result if result else None
        except Exception as e:
            logger.error(f"Error retrieving video info: {e}")
            raise

async def update_terabox_link_caption(reference_id, new_caption):
    async with aiosqlite.connect(config.DB_NAME) as db:
        try:
            await db.execute('''UPDATE terabox_links
                                SET new_caption = ?
                                WHERE id = ?''',
                             (new_caption, reference_id))
            await db.commit()
        except Exception as e:
            logger.error(f"Error updating terabox link caption: {e}")
            raise