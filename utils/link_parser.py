
import re

def parse_terabox_links(text):
    if not text:
        return []
    url_pattern = r'https?://[^\s]*terabox[^\s]*'
    return re.findall(url_pattern, text)