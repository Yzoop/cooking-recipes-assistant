import requests
from bs4 import BeautifulSoup
from urllib3.util import url


def get_website_context(website_url: url) -> str:
    # TODO: handle bot detection
    response = requests.get(website_url)
    # TODO: add proper error handling
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.text
    while "\n\n" in content or "\t\t" in content:
        content = content.replace("\n\n", "\n").replace("\t\t", "\t")
    return content
