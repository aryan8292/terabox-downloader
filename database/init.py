import aiosqlite
from config import load_config

async def init_database():
    config = load_config()
    async with aiosqlite.connect(config.DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS terabox_links
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            file_type TEXT,
                            sizes TEXT,
                            original_caption TEXT,
                            new_caption TEXT,
                            original_thumbnail TEXT,
                            unique_string TEXT)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS video_info
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            reference_id INTEGER,
                            user_id INTEGER,
                            unique_str TEXT,
                            argument TEXT,
                            FOREIGN KEY (reference_id) REFERENCES terabox_links(id))''')
        await db.commit()