import requests
from typing import Union
from requests import Response


def chase_redirects(url: Union[list, str]) -> list[str]:
    _urls = []

    def _chase(url: str):
        resp: Response = requests.head(url)
        if 300 < resp.status_code < 400:
            return resp.headers["location"]

    if isinstance(url, list):
        for each in url:
            _urls.append(_chase(each))

    if isinstance(url, str):
        _urls.append(_chase(url))

    return _urls


# url = ["https://t.co/xRhOZeNJLe", "https://t.co/Dy33xpoxAV"]
# ret = chase_redirects(url)
# print(ret)
