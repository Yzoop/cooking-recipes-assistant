import re
from enum import StrEnum

import requests
from bs4 import BeautifulSoup
from pydantic import HttpUrl


class UrlType(StrEnum):
    web_page_url = "WEB_PAGE_URL"
    tiktok_url = "TIKTOK_URL"
    unknown = "UNKNOWN"


def get_website_context(website_url: HttpUrl) -> str:
    # TODO: handle bot detection
    # TODO: reduce content size for api input size sake
    response = requests.get(website_url)
    # TODO: add proper error handling
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.text
    while "\n\n" in content or "\t\t" in content:
        content = content.replace("\n\n", "\n").replace("\t\t", "\t")
    return content


def type_of_url(url: HttpUrl) -> UrlType:
    """
    Identifies the type of the given URL.
    :param url: The URL to check.
    :return: UrlType.web_page_url for regular webpages, UrlType.tiktok_url for TikTok URLs.
    :raises NotImplementedError: If the URL type is not implemented.
    """
    if "tiktok.com" in str(url):
        return UrlType.tiktok_url
    elif re.match(r"https?://", str(url)):
        return UrlType.web_page_url
    else:
        return UrlType.unknown
