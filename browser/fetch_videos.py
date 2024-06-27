import aiohttp
import asyncio
import logging
import json
import re
import uuid
import os
from aiohttp import ClientSession
from asyncio import Semaphore

session = None
semaphore = None

async def init_session(max_concurrent_downloads=5):
    global session, semaphore
    session = aiohttp.ClientSession(headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    semaphore = Semaphore(max_concurrent_downloads)

async def close_session():
    if session:
        await session.close()

async def getVideo(links):
    tasks = [fetch_video_info(link) for link in links]
    return await asyncio.gather(*tasks)

async def fetch_video_info(link):
    async with semaphore:
        finalLink = f'https://tera.instavideosave.com/?url={link}'
        try:
            async with session.post(finalLink, timeout=10) as response:
                response.raise_for_status()
                json_content = await response.text()
                return extract_data(json_content)
        except aiohttp.ClientError as e:
            logging.error(f"Error while fetching video info: {str(e)}")
            return " "

def extract_data(json_content):
    try:
        data = json.loads(json_content)
        return data['video'][0]['video']
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        logging.error(f"Error extracting data: {str(e)}")
        return None

async def getFileInfo(link):
    try:
        async with session.head(link, timeout=10) as response:
            content_length = int(response.headers.get("Content-Length", 0))
            filename = response.headers.get('Content-Disposition', '').split('filename=')[-1].strip('"') or f"{uuid.uuid4()}.mp4"
            return content_length / (1024 * 1024), filename
    except aiohttp.ClientError as e:
        logging.error(f"Error while getting the size info: {str(e)}")
        return None, None

async def download_video(link, filename, chunk_size=1024*1024):
    directory = "data/videos"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)

    try:
        async with session.get(link, timeout=60*2) as response:
            if response.status == 200:
                with open(file_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        f.write(chunk)
                logging.info(f"Video downloaded and saved as {file_path}")
                return file_path
            else:
                logging.error(f"Failed to download video. Status code: {response.status}")
    except asyncio.TimeoutError:
        logging.error(f"Timeout occurred while downloading video")
    except aiohttp.ClientError as e:
        logging.error(f"Error while downloading video: {str(e)}")
    return None