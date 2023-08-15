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
        # load()������fp(һ��֧��.read()���ļ�����󣬰���һ��JSON�ĵ�)�����л�Ϊһ��Python����
        return yaml.safe_load(fp)


