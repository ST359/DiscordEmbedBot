import urllib.parse
import re

regex = r"(?:\s|^)(https?://(?:www\.)?(?:twitter\.com|instagram\.com)/\S+)"
instagram_url = 'www.instagram.com'
twitter_url = 'twitter.com'
instagram_url_embeddable = 'www.ddinstagram.com'
twitter_url_embeddable = 'vxtwitter.com'


def extract_url_from_message(message: str) -> list | None:
    urls_to_parse = re.findall(regex, message)
    urls = [urllib.parse.urlparse(url) for url in urls_to_parse]
    return urls


def make_url_embeddable(url_in: list) -> list:
    urls_out = []
    for url in url_in:
        if url.netloc == twitter_url:
            new_url = url._replace(netloc=twitter_url_embeddable)
            urls_out.append(urllib.parse.urlunparse(new_url))
        elif url.netloc == instagram_url:
            new_url = url._replace(netloc=instagram_url_embeddable)
            urls_out.append(urllib.parse.urlunparse(new_url))
    return urls_out
