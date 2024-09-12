# -*- coding: utf-8 -*-
import requests
import yaml


def request(url, methods, **kwargs):
    methods = methods.lower()
    if methods == "get":
        res = requests.Session().get(url, **kwargs)
        return res
    elif methods == "post":
        res = requests.Session().post(url, **kwargs)
        return res


def SseOptionQuote(url, headers, **kwargs):
    try:
        response = requests.Session().get(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error while requesting url '{url}':{e}")
        return None


def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        # load()锟斤拷锟斤拷锟斤拷fp(一锟斤拷支锟斤拷.read()锟斤拷锟侥硷拷锟斤拷锟斤拷螅锟斤拷锟揭伙拷锟絁SON锟侥碉拷)锟斤拷锟斤拷锟叫伙拷为一锟斤拷Python锟斤拷锟斤拷
        return yaml.safe_load(fp)


