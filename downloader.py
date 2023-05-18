#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author : djs
# @project: work_code
# @file   : downloader.py
# @time   : 2023/5/15 11:51
# @desc   : None
from yarl import URL
from rainbow_console import console, options
from elegant_spider.response import Response, convert
from elegant_spider.utils.ja3 import aiohttp_ssl, requests_session


class Downloader:
    def request_parameters(self) -> dict:
        parameters = {
            'url': getattr(self, 'request_url', None),
            'method': getattr(self, 'method', None),
            'data': getattr(self, 'data', None),
            'json': getattr(self, 'json', None),
            'files': getattr(self, 'files', None),
            'headers': getattr(self, 'headers', None),
            'cookies': getattr(self, 'cookies', None),
        }
        return {key: value for key, value in parameters.items() if value}

    @staticmethod
    def put_cookies_in_headers(parameters: dict) -> dict:
        if 'cookies' in parameters:
            cookies = "; ".join(['%s=%s' % (key, value) for key, value in parameters['cookies'].items()])
            parameters['headers'] = parameters.get('headers', {})
            parameters['headers']['Cookies'] = cookies
            del parameters['cookies']
        return parameters

    def request(
            self,
            timeout: int or float = 180,
            proxies: dict = None,
            verify: bool = None,
            allow_redirects: bool = True,
            ja3: bool = False,
    ) -> Response:
        try:
            import requests
        except ImportError:
            print(console.text('pip install requests', options.ForegroundColor.YELLOW))
            raise

        if ja3:
            request = ja3 and requests_session(getattr(self, 'baseurl')).request
        else:
            request = requests.request

        kwargs = self.put_cookies_in_headers(self.request_parameters())
        response = request(
            **kwargs, timeout=timeout, proxies=proxies, verify=verify, allow_redirects=allow_redirects
        )
        return convert(response)

    async def async_request(
            self,
            timeout: int or float = 5 * 60,
            proxy: str = None,
            verify_ssl: bool = None,
            allow_redirects: bool = True,
            ja3: bool = False,

    ) -> Response:
        try:
            import aiohttp
        except ImportError:
            print(console.text('pip install aiohttp', options.ForegroundColor.YELLOW))
            raise

        if ja3:
            ssl = aiohttp_ssl()
        else:
            ssl = None

        kwargs = self.put_cookies_in_headers(self.request_parameters())
        kwargs['url'] = URL(kwargs['url'], encoded=True)
        assert 'files' not in kwargs, 'files is aiohttp unsupport parameter'

        async with aiohttp.ClientSession() as session:
            timeout = aiohttp.ClientTimeout(total=timeout)
            response = await session.request(
                **kwargs, timeout=timeout, proxy=proxy, verify_ssl=verify_ssl, allow_redirects=allow_redirects, ssl=ssl
            )
            await response.read()
            return convert(response)
