import urllib.parse
import re
import requests
import httpx
from bs4 import BeautifulSoup

regex_post_not_found = r"(content=\"Post not found\"|content=\"Post might not be available\")"
regex_not_spoiler = r"(https?://(?:www\.)?(?:twitter\.com|instagram\.com|x\.com)/[^\|\s]+)"
regex_not_spoiler_ddinsta = r"(https?://(?:www\.)?(?:ddinstagram\.com)/[^\|\s]+)"
regex_spoiler = r"(?:(?<=\|\|\s)|(?<=\|\|))(https?://(?:www\.)?(?:twitter\.com|instagram\.com|x\.com)/\S+)(?=\s*\|\|)"
instagram_url = ('www.instagram.com', 'instagram.com')
twitter_url = ('twitter.com', 'x.com')
instagram_url_embeddable = 'www.ddinstagram.com'
instagram_url_embeddable_backup = 'www.instagramez.com'
twitter_url_embeddable = 'vxtwitter.com'


def extract_url_from_message(message: str) -> tuple:
    raw_urls = re.findall(regex_not_spoiler, message)
    parsed_urls = [urllib.parse.urlparse(url) for url in raw_urls]
    return raw_urls, parsed_urls


def does_contain_urls(message: str) -> bool:
    if len(extract_url_from_message(message)[0]) > 0:
        return True
    return False


def is_ddinsta_url_working(url: str) -> bool:
    try:
        r = requests.get(url).text
        if re.search(regex_post_not_found, r):
            return False
    except:
        return False
    return True


async def is_ddinsta_url_working_async(url: str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url)
            if re.search(regex_post_not_found, r.text) or r.status_code != 200:
                return False
            else:
                return True
        except:
            return False


async def make_url_embeddable(url_in: list) -> list:
    urls_out = []
    for url in url_in:
        if url.netloc in twitter_url:
            new_url = url._replace(netloc=twitter_url_embeddable)
            urls_out.append(urllib.parse.urlunparse(new_url))
        elif url.netloc in instagram_url:
            if "share" in url.path:
                final_id = get_final_reel_id(urllib.parse.urlunparse(url))
                final_path = "/reel/"+final_id
                url = url._replace(path=final_path)
            new_url = url._replace(netloc=instagram_url_embeddable)
            is_working = await is_ddinsta_url_working_async(urllib.parse.urlunparse(new_url))
            if is_working:
                urls_out.append(urllib.parse.urlunparse(new_url))
            else:
                new_url = url._replace(netloc=instagram_url_embeddable_backup)
                urls_out.append(urllib.parse.urlunparse(new_url))
    return urls_out


def replace_urls_with_embeddables(message_in: str, raw_urls: list, embeddable_urls: list) -> str:
    new_message = message_in
    for old_url, new_url in zip(raw_urls, embeddable_urls):
        new_message = new_message.replace(old_url, new_url)
    return new_message

def get_final_reel_id(share_url) ->str:
    response = requests.get(share_url)

    if response.status_code == 200:
        final_url = response.url
        reel_id = final_url.split('/')[-2]  # The reel ID is the second to last component
        return reel_id
    else:
        print(f"Failed to fetch page: {response.status_code}")
        return ""