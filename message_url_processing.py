import urllib.parse
import re
import requests

regex_post_not_found = r"(content=\"Post not found\")"
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
    r = requests.get(url).text
    if re.search(regex_post_not_found, r):
        return False
    return True
def make_url_embeddable(url_in: list) -> list:
    urls_out = []
    for url in url_in:
        if url.netloc in twitter_url:
            new_url = url._replace(netloc=twitter_url_embeddable)
            urls_out.append(urllib.parse.urlunparse(new_url))
        elif url.netloc in instagram_url:
            new_url = url._replace(netloc=instagram_url_embeddable)
            if is_ddinsta_url_working(urllib.parse.urlunparse(new_url)):
                urls_out.append(urllib.parse.urlunparse(new_url))
            else:
                new_url = url._replace(netloc =instagram_url_embeddable_backup)
                urls_out.append(urllib.parse.urlunparse(new_url))
    return urls_out

def replace_urls_with_embeddables(message_in: str, raw_urls: list, embeddable_urls: list) -> str:
    new_message = message_in
    for old_url, new_url in zip(raw_urls, embeddable_urls):
        new_message = new_message.replace(old_url, new_url)
    return new_message
