from pyrogram import Client
from pyrogram.types import Message
from utils.state_manager import get_state_manager
from .terabox_handlers import handle_terabox_message
from .button_handlers import handle_level1_buttons, handle_level2_buttons

async def message_handler(client: Client, message: Message):
    state_manager = get_state_manager()
    user_state = state_manager.get_user_state(message.from_user.id)

    if user_state == "level1":
        await handle_level1_buttons(client, message)
    elif user_state == "level2":
        await handle_level2_buttons(client, message)
    elif user_state == "level3":
        await handle_terabox_message(client, message)