from enum import Enum
import re
import requests
import sys
import json
from urllib.parse import urlparse, urlencode, quote, urljoin
from datetime import timedelta
from hashlib import sha256
from typing import Literal, Required, TypedDict

import py_common.log as log
from py_common.util import scraper_args
from py_common.types import ScrapedScene, ScrapedPerformer, ScrapedTag

# See https://coomer.su/api/schema
API_URL = "https://coomer.su/api/v1"

class CoomerService(Enum):
    ONLYFANS = "onlyfans"
    FANSLY = "fansly"
    CANDFANS = "candfans"

class FileResponse(TypedDict):
    name: str
    path: str

class PostResponse(TypedDict):
    id: int
    file_id: int
    user: Required[str] # user-id
    service: Required[str]
    title: Required[str | None]
    substring: Required[str | None]
    published: Required[str]
    file: FileResponse
    attachments: list[FileResponse]


class SearchHashResponse(TypedDict):
    # GET /search_hash/{file_hash} response
    id: int
    hash: Required[str]
    mtime: str
    ctime: str
    mime: str
    ext: str
    added: str
    size: int
    ihash: str | None
    posts: Required[list[PostResponse]]

class GetCreatorResponse(TypedDict):
    id: Required[str]
    name: Required[str]
    service: Required[str]
    indexed: str
    updated: str
    public_id: str | None
    relation_id: int

class CoomerAPI:
    def __init__(self, api_base_url: str) -> None:
        self.api_base_url: str = api_base_url

    def get_creator(self, user: str) -> GetCreatorResponse:
        # url = urljoin(self.api_base_url, user, "/profile")
        res: GetCreatorResponse = {}
        return res

    def search_hash(self, hash_sha256: str) -> SearchHashResponse:
        res: SearchHashResponse = {}
        return res

def to_scraped_performer(user: str, service: str):
    performer: ScrapedPerformer = {"name": ""}

    if service == CoomerService.FANSLY:
        # Coomer's scraping of Fansly uses an id for the username

def to_scraped_scene(post: PostResponse) -> ScrapedScene:
    # add the service (e.g. "onlyfans") as a tag
    service_tag: ScrapedTag = {"name": post["service"]}

    performer: ScrapedPerformer = {"name": ""}

    scene: ScrapedScene = {
        "title": post["title"],
        # "details": str
        # "url": str
        # "urls": list[str]
        # "date": str
        # "image": str
        # studio: ScrapedStudio
        # movies: list[ScrapedMovie]
        "tags": [service_tag],
        "performers": [performer],
        # code: str
        # director: str
    }

    # title and substring are often the same, but if they're not, then use substring as scene details
    if post["title"] != post["substring"]:
        scene["details"] = post["substring"]

    return scene


def scene_from_fragment(title: str) -> ScrapedScene | None:
    log.debug(f"Getting scene through fragment title: '{title}'")


if __name__ == "__main__":
    op, args = scraper_args()

    result = None

    match op, args:
        # case "scene-by-name", {"name": name} if name:
        #     result = scene_search(name)
        case "scene-by-fragment", {"title": title}:
            result = scene_from_fragment(title)
        # case "performer-by-url" | "performer-by-fragment", {"url": url}:
        #     result = performer_from_url(url)
        case _:
            log.error(f"Operation: {op}, arguments: {json.dumps(args)}")
            sys.exit(1)

    print(json.dumps(result))
