from pyrogram import Client
from pyrogram.types import Message
from utils.menu_buttons import adminKeyboard1, adminKeyboard2, goBackKeyBoard, LinkConverterTxt, teraboxTxt, uploadVidTxt, goBackTxt
from utils.state_manager import get_state_manager

async def handle_level1_buttons(client: Client, message: Message):
    state_manager = get_state_manager()
    if message.text == LinkConverterTxt:
        await client.send_message(chat_id=message.chat.id, text="Choose an option:", reply_markup=adminKeyboard2)
        state_manager.set_user_state(message.from_user.id, "level2")
    elif message.text == goBackTxt:
        await client.send_message(chat_id=message.chat.id, text="Main menu", reply_markup=adminKeyboard1)
        state_manager.set_user_state(message.from_user.id, "level1")
    else:
        await client.send_message(chat_id=message.chat.id, text="Invalid option. Please try again.", reply_markup=adminKeyboard1)

async def handle_level2_buttons(client: Client, message: Message):
    state_manager = get_state_manager()
    if message.text == teraboxTxt:
        await client.send_message(chat_id=message.chat.id, text="Send me posts with TeraBox links.", reply_markup=goBackKeyBoard)
        state_manager.set_user_state(message.from_user.id, "level3")
    elif message.text == uploadVidTxt:
        await client.send_message(chat_id=message.chat.id, text="Send me videos and I will generate links for you.",reply_markup=goBackKeyBoard)
    elif message.text == goBackTxt:
        await client.send_message(chat_id=message.chat.id, text="Main menu", reply_markup=adminKeyboard1)
        state_manager.set_user_state(message.from_user.id, "level1")
    else:
        await client.send_message(chat_id=message.chat.id, text="Invalid option. Please try again.", reply_markup=adminKeyboard2)