from pyrogram import Client
from pyrogram.types import Message
from utils.menu_buttons import adminKeyboard1
from database.operations import retrieve_video_info
from utils.logging import get_logger
from utils.state_manager import get_state_manager

logger = get_logger(__name__)

async def start_handler(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text="Welcome to TeraBox Downloader!",
        reply_markup=adminKeyboard1
    )
    state_manager = get_state_manager()
    state_manager.set_user_state(message.from_user.id, "level1")
    
    if len(message.command) > 1:
        argument = message.command[1]
        try:
            video_info = await retrieve_video_info(argument)
            if video_info:
                await client.send_video(chat_id=message.chat.id, video=video_info[0])
            else:
                await client.send_message(chat_id=message.chat.id, text="Video not found.")
        except Exception as e:
            logger.error(f"Error sending video: {e}")
            await client.send_message(chat_id=message.chat.id, text="An error occurred while processing your request.")