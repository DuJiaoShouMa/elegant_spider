#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author : djs
# @project: sz0518
# @file   : setup.py
# @time   : 2023/5/17 18:14
# @desc   : None
from setuptools import setup, find_packages

setup(
    name='elegant_spider',
    version='1.0.0',
    description='A Elegant Spider',
    url='https://github.com/DuJiaoShouMa/elegant_spider',
    author='djs',
    author_email='',
    packages=find_packages(),
    install_requires=[
        # List your package's dependencies here
        'urllib3 >= 1.26.2',
    ],
)
