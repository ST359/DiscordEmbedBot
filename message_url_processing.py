import urllib.parse
import re

regex_not_spoiler = r"(https?://(?:www\.)?(?:twitter\.com|instagram\.com|x\.com)/[^\|\s]+)"
regex_spoiler = r"(?:(?<=\|\|\s)|(?<=\|\|))(https?://(?:www\.)?(?:twitter\.com|instagram\.com|x\.com)/\S+)(?=\s*\|\|)"
instagram_url = ('www.instagram.com', 'instagram.com')
twitter_url = ('twitter.com', 'x.com')
instagram_url_embeddable = 'www.ddinstagram.com'
twitter_url_embeddable = 'vxtwitter.com'


def extract_url_from_message(message: str) -> tuple:
    raw_urls = re.findall(regex_not_spoiler, message)
    parsed_urls = [urllib.parse.urlparse(url) for url in raw_urls]
    return raw_urls, parsed_urls


def does_contain_urls(message: str) -> bool:
    if len(extract_url_from_message(message)[0]) > 0:
        return True
    return False


def make_url_embeddable(url_in: list) -> list:
    urls_out = []
    for url in url_in:
        if url.netloc in twitter_url:
            new_url = url._replace(netloc=twitter_url_embeddable)
            urls_out.append(urllib.parse.urlunparse(new_url))
        elif url.netloc in instagram_url:
            new_url = url._replace(netloc=instagram_url_embeddable)
            urls_out.append(urllib.parse.urlunparse(new_url))
    return urls_out


def replace_urls_with_embeddables(message_in: str, raw_urls: list, embeddable_urls: list) -> str:
    new_message = message_in
    for old_url, new_url in zip(raw_urls, embeddable_urls):
        new_message = new_message.replace(old_url, new_url)
    return new_message
