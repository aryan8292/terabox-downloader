import asyncio
import re
import uuid
import logging
from pyrogram import Client
from pyrogram.types import Message
from browser.fetch_videos import getVideo, download_video, getFileInfo
from database.operations import insert_terabox_links, insert_video_info, update_terabox_link_caption
from utils.menu_buttons import adminKeyboard1, goBackTxt
from utils.state_manager import get_state_manager
from utils.link_parser import parse_terabox_links
import time
from config import load_config

logger = logging.getLogger(__name__)

config = load_config()
last_update_time = 0

async def handle_terabox_message(client: Client, message: Message):
    links = parse_terabox_links(message.caption or message.text)
    if not links:
        if message.text == goBackTxt:
            state_manager = get_state_manager()
            state_manager.set_user_state(message.from_user.id, "level1")
            await client.send_message(chat_id=message.chat.id, text="Main menu", reply_markup=adminKeyboard1)
        else:
            await client.send_message(chat_id=message.chat.id, text="No valid TeraBox links found.", reply_to_message_id=message.id)
        return

    status_message = await client.send_message(chat_id=message.chat.id, text="Processing TeraBox links...", reply_to_message_id=message.id)
    
    try:
        downloadable_links = await getVideo(links)
        
        sizes = []
        special_strings = []
        new_links = []
        success_count = 0

        async def progress_callback(current, total):
            try:
                global last_update_time
                current_time = time.time()
                if current_time - last_update_time > 3:
                    last_update_time = current_time
                    await client.edit_message_text(
                        chat_id=status_message.chat.id,
                        message_id=status_message.id,
                        text=f"Uploading: {current * 100 / total:.1f}%"
                    )
            except Exception as e:
                logger.error(f"Error updating progress: {e}")

        for i, link in enumerate(downloadable_links):
            try:
                if link != " ":
                    size, filename = await getFileInfo(link)
                    sizes.append(size)

                    if 0.01 < size < 20:
                        try:
                            video_message = await client.send_video(chat_id=config.DUMMY_ID, video=link)
                            special_string = video_message.video.file_id
                        except:
                            await client.edit_message_text(chat_id=status_message.chat.id, message_id=status_message.id, text=f"Downloading video {i+1}...")
                            file_path = await download_video(link, filename)
                            video_message = await client.send_video(
                                chat_id= config.DUMMY_ID,
                                video=file_path,
                                progress= progress_callback
                            )
                        special_string = video_message.video.file_id
                    elif 20 <= size < 500:
                        await client.edit_message_text(chat_id=status_message.chat.id, message_id=status_message.id, text=f"Downloading video {i+1}...")
                        file_path = await download_video(link, filename)
                        video_message = await client.send_video(
                            chat_id= config.DUMMY_ID,
                            video=file_path,
                            progress= progress_callback
                        )
                        special_string = video_message.video.file_id
                    else:
                        await client.send_message(chat_id=message.chat.id, text=f"Video {i+1} is too large to process. For large videos try uploading the video directly in Generate Link from Video button")
                        special_string = None

                    special_strings.append(special_string)
                    
                    if special_string:
                        argument = str(uuid.uuid4()).replace("-", "")
                        new_link = f"t.me/{config.BOT_USERNAME}?start={argument}"
                        new_links.append((links[i], new_link, argument, special_string))
                        success_count += 1
                    else:
                        new_links.append((links[i], " ", None, None))
                else:
                    sizes.append(-1)
                    special_strings.append(None)
                    new_links.append((links[i], " ", None, None))
            except Exception as e:
                logger.error(f"Error processing link {i+1}: {e}")
                sizes.append(-1)
                special_strings.append(None)
                new_links.append((links[i], " ", None, None))

        if success_count == 0:
            await client.edit_message_text(chat_id=status_message.chat.id, message_id=status_message.id, text="Failed to process all links. Please try again later.")
            return
        
        # Prepare data for database insertion
        user_id = message.from_user.id
        file_type = "photo" if message.photo else "video" if message.video else "text"
        original_caption = message.caption or message.text
        original_thumbnail = message.photo.file_id if message.photo else message.video.file_id if message.video else None
        
        sizes_str = " ".join(f"{size:.2f}" for size in sizes)
        special_strings_str = " ".join(s if s else " " for s in special_strings)

        # Insert into terabox_links table
        reference_id = await insert_terabox_links(user_id, file_type, sizes_str, original_caption, original_thumbnail, special_strings_str)
        
        # Insert into video_info table and create new caption
        new_caption = original_caption
        for old_link, new_link, argument, special_string in new_links:
            if argument and special_string:
                await insert_video_info(user_id, reference_id, special_string, argument)
                new_caption = new_caption.replace(old_link, new_link)
            else:
                new_caption = new_caption.replace(old_link, " ")

        await update_terabox_link_caption(reference_id, new_caption)

        new_caption = " " + new_caption + " "

        # Send the processed message back to the user
        if file_type == "text":
            await client.send_message(chat_id=message.chat.id, text=new_caption)
        elif file_type == "photo":
            await client.send_photo(chat_id=message.chat.id, photo=original_thumbnail, caption=new_caption)
        elif file_type == "video":
            await client.send_video(chat_id=message.chat.id, video=original_thumbnail, caption=new_caption)

        await client.delete_messages(chat_id=status_message.chat.id, message_ids=status_message.id)

    except Exception as e:
        logger.error(f"Error processing TeraBox links: {e}")
        await client.edit_message_text(chat_id=status_message.chat.id, message_id=status_message.id, text="An error occurred while processing the links.")

