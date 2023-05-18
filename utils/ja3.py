#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author : djs
# @project: work_code
# @file   : ja3.py
# @time   : 2023/5/15 15:04
# @desc   : None
import copy
import random

ORIGIN_CIPHERS = [
    'ECDH+AESGCM',
    'DH+AESGCM',
    'ECDH+AES256',
    'DH+AES256',
    'ECDH+AES128',
    'DH+AES',
    'ECDH+HIGH',
    'DH+HIGH',
    'ECDH+3DES',
    'DH+3DES',
    'RSA+AESGCM',
    'RSA+AES',
    'RSA+HIGH',
    'RSA+3DES'
]


def ciphers():
    _ciphers = copy.deepcopy(ORIGIN_CIPHERS)
    random.shuffle(_ciphers)
    _ciphers = ':'.join(_ciphers)
    _ciphers += ":!aNULL:!eNULL:!MD5"
    return _ciphers


def aiohttp_ssl():
    import ssl
    context = ssl.create_default_context()
    context.set_ciphers(ciphers())
    return context


def requests_session(domain: str):
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.ssl_ import create_urllib3_context

    context = create_urllib3_context(ciphers=ciphers())

    class DESAdapter(HTTPAdapter):
        def init_poolmanager(self, *args, **kwargs):
            kwargs['ssl_context'] = context
            return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

        def proxy_manager_for(self, *args, **kwargs):
            kwargs['ssl_context'] = context
            return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)

    session = requests.Session()
    session.mount(domain, DESAdapter())
    return session
