#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="py-pasebin",
    version="0.1",
    packages=find_packages(),
    scripts=['py-pastebin.py'],
    install_requires=['requests'],
)
