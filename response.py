#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author : djs
# @project: work_code
# @file   : response.py
# @time   : 2023/5/15 15:07
# @desc   : None
import re
import json
import typing
from rainbow_console import console, options


class Response:
    def __init__(
            self,
            response,
            url: str,
            status_code: int,
            content: bytes,
            text: str,
            jsondata: typing.Union[dict, list, None],
            headers: dict,
            cookies: dict,
    ):
        self.response = response
        self.url = url
        self.status_code = self.status = status_code
        self.content = content or text.encode()
        self.text = text
        self.headers = headers
        self.cookies = cookies
        self.jsondata = jsondata
        self._html = None

    def json(self) -> dict or list:
        return self.jsondata or json.loads(self.text)

    def xpath(self, _xpath: str):
        if self._html is None:
            try:
                from lxml import etree
            except ImportError:
                print(console.text('pip install lxml', options.ForegroundColor.YELLOW))
                raise
            self._html = etree.HTML(self.text)

        return self._html.xpath(_xpath)


def convert(response, body: bytes = None) -> Response:
    if repr(type(response)) in [
        "<class 'aiohttp.client_reqrep.ClientResponse'>"
    ]:
        if body is None:
            content = getattr(response, '_body', None)
            if content is None:
                raise ValueError('need to await response.read() before this, or content is null')
        else:
            content = body

        headers = dict(response.headers)
        if 'Set-Cookie' in headers:
            del headers['Set-Cookie']

        return Response(
            response=response,
            url=str(response.url),
            status_code=response.status,
            content=content,
            text=content.decode(response.get_encoding()),
            jsondata=None,
            headers=headers,
            cookies={ck: cookie.value for ck, cookie in response.cookies.items()}
        )
    elif repr(type(response)) in [
        "<class 'scrapy.http.response.text.TextResponse'>",
        "<class 'scrapy.http.response.html.HtmlResponse'>"
    ]:
        cookies = {}
        for cookie in response.headers.getlist('Set-Cookie'):
            ck, cv = re.findall(r'^(.*)=(.*)$', cookie.decode().split(';')[0])[0]
            cookies[ck] = cv

        # response.headers
        headers = dict(response.headers.to_unicode_dict())
        for rk in ['set-cookie', 'Set-Cookie']:
            if rk in headers:
                del headers[rk]

        return Response(
            response=response,
            url=response.url,
            status_code=response.status,
            content=response.body,
            text=response.text,
            jsondata=None,
            headers=headers,
            cookies=cookies
        )
    else:
        try:
            import requests.utils
        except ImportError:
            print(console.text('pip install requests', options.ForegroundColor.YELLOW))
            raise
        return Response(
            response=response,
            url=response.url,
            status_code=response.status_code,
            content=response.content,
            text=response.text,
            jsondata=None,
            headers=dict(response.headers),
            cookies=requests.utils.dict_from_cookiejar(response.cookies)
        )
