#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="py-pasebin",
    version="0.1",
    packages=find_packages(),
    scripts=['py-pastebin.py'],
    install_requires=['requests'],

    author="Radoslaw Smigielski",
    author_email="",
    description="py-pastebin cmd tool to create new pastes on pastebin.com",
    license="GPL",
    keywords="paste pastebin",
    url="https://github.com/radeksm/py-pastebin",
    project_urls={
        "Bug Tracker": "https://github.com/radeksm/py-pastebin/issues",
        "Documentation": "https://github.com/radeksm/py-pastebin/blob/master/README.md",
        "Source Code": "https://github.com/radeksm/py-pastebin",
    }
)
