# handlers/__init__.py
from .start import start_handler
from .message import message_handler
from pyrogram import filters

def register_handlers(app):
    app.on_message(filters.command("start"))(start_handler)
    app.on_message(~filters.command("start"))(message_handler)

# Explicitly expose the register_handlers function
__all__ = ['register_handlers']