#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author : djs
# @project: work_code
# @file   : spider.py
# @time   : 2023/5/11 14:27
# @desc   : from xueao bro simple_spider project
from urllib.parse import urlencode
from elegant_spider.downloader import Downloader


class MetaSpider(type):
    def __new__(mcs, name, bases, attrs):
        for pro in ('params', 'data', 'json', 'files', 'headers', 'cookies'):
            if pro in attrs:
                attrs[pro] = property(attrs[pro])
        # if 'parse' in attrs:
        #     attrs['parse'] = parse_displayer(attrs['parse'])
        return type.__new__(mcs, name, bases, attrs)


class Spider(Downloader, metaclass=MetaSpider):
    def __init__(self, url: str, method: str = 'GET'):
        assert url.startswith('http://') or url.startswith('https://'), 'url "%s" is not vaild url' % url
        assert method.upper() in ['GET', 'POST'], 'method "%s" is not vaild method' % method
        self.url = url
        self.method = method

    @property
    def request_url(self):
        params = self.params
        if params and isinstance(params, dict):
            return self.url + '?' + urlencode(params)
        return self.url

    def params(self):
        pass

    def data(self):
        pass

    def json(self):
        pass

    def files(self):
        pass

    def headers(self):
        pass

    def cookies(self):
        pass

    def parse(self, response, pretty_print: bool = False):
        """

        :param bool pretty_print:
        :param Response response:
        :return:
        """
        pass