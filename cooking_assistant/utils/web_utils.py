import json
import os
import re
import tempfile
from enum import StrEnum
from pathlib import Path

import browser_cookie3
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from moviepy import VideoFileClip
from openai import OpenAI
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


class TikTokManager:
    cookies = dict()
    headers = {
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "en-US,en;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Cache-Control": "max-age=0",
        "refer": "https://www.tiktok.com/",
        "Connection": "keep-alive",
    }
    context_dict = {
        "viewport": {"width": 0, "height": 0},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.150 Safari/537.36",
    }

    def __init__(self, openai_api_key_name: str = "OPENAI_API_KEY"):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv(openai_api_key_name))
        # pyk.specify_browser("chrome")

    def get_tiktok_captions(self, tt_video_url: HttpUrl) -> str:
        temp_dir = tempfile.TemporaryDirectory()
        try:
            print(f"Downloading the given tiktok video: {tt_video_url}")
            tt_video_path, tt_video_desc = self.__download_video(
                tt_video_url, where_to_save=Path(temp_dir.name)
            )
            print(f"Video downloaded at path: {tt_video_path}")
            print("Extracting audio...")
            audio_path = self.__extract_audio(
                video_path=tt_video_path, save_dir=Path(temp_dir.name)
            )
            print(f"Extracted audio from the video: {tt_video_path}; saved to {audio_path}")
            captions = self.__get_captions_from_audio(audio_path)
            captions_with_description = f"Description: {tt_video_desc}\n{captions}"
            # use temp_dir, and when done:
        except Exception as e:
            print(e)
            raise Exception(e)
        finally:
            temp_dir.cleanup()
        return captions_with_description

    def __get_captions_from_audio(self, audio_path: Path):
        with open(audio_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1", file=audio_file
            )
        return transcription.text

    def __extract_audio(self, video_path: Path, save_dir: Path) -> Path:
        video_clip = VideoFileClip(video_path)

        audio_clip = video_clip.audio

        mp3_path = save_dir / Path("audio.mp3")
        audio_clip.write_audiofile(mp3_path)

        audio_clip.close()
        video_clip.close()

        return mp3_path

    def __alt_get_tiktok_json(self, video_url, browser_name=None):
        # if 'cookies' not in globals() and browser_name is None:
        #     raise BrowserNotSpecifiedError
        if browser_name is not None:
            TikTokManager.cookies = getattr(browser_cookie3, browser_name)(
                domain_name="www.tiktok.com"
            )
        tt = requests.get(
            video_url, headers=TikTokManager.headers, cookies=TikTokManager.cookies, timeout=20
        )
        # retain any new cookies that got set in this request
        TikTokManager.cookies = tt.cookies
        soup = BeautifulSoup(tt.text, "html.parser")
        tt_script = soup.find("script", attrs={"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
        try:
            tt_json = json.loads(tt_script.string)
        except AttributeError:
            print(
                "The function encountered a downstream error and did not deliver any data, "
                "which happens periodically for various reasons. Please try again later."
            )
            return
        return tt_json

    def __download_video(
        self, tt_video_url: HttpUrl, where_to_save: Path, browser_name=None
    ) -> (Path, str):
        """
        Download video locally, saves as a temorary file
        :return: path to the video, downloaded from given url. Video description as str
        """
        video_fn = where_to_save / Path("tt_video.mp4")

        tt_json = self.__alt_get_tiktok_json(str(tt_video_url), browser_name)
        tt_video_url = tt_json["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"][
            "itemStruct"
        ]["video"]["playAddr"]
        tt_video_description = tt_json["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"][
            "itemStruct"
        ]["desc"]
        if tt_video_url == "":
            tt_video_url = tt_json["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"][
                "itemStruct"
            ]["video"]["downloadAddr"]
        # include cookies with the video request
        tt_video = requests.get(
            tt_video_url,
            allow_redirects=True,
            headers=TikTokManager.headers,
            cookies=TikTokManager.cookies,
        )
        with open(video_fn, "wb") as fn:
            fn.write(tt_video.content)
        return video_fn, tt_video_description
