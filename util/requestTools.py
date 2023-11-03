import requests

from util.logTool import logger


def request(url, methods, **kwargs):
    methods = methods.lower()
    if methods == "get":
        res = requests.Session().get(url, **kwargs)
        return res
    elif methods == "post":
        res = requests.Session().post(url, **kwargs)
        return res


def SseOptionQuote(url, header, **kwargs):
    try:
        response = requests.Session().get(url, headers=header)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.debug(f"Error while requesting url '{url}':{e}")
        logger.debug(f"Error while request headers '{header}':{e}")
        return None