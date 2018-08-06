#!/usr/bin/env python3

""" Full API specification: https://pastebin.com/api#2

Options:
   
   # access 0=public 1=unlisted 2=private

"""

import argparse
import configparser
import logging
import os
import requests
import sys

from http.client import HTTPConnection
from io import StringIO


URL_LOGIN = 'https://pastebin.com/api/api_login.php'
URL_PASTE = 'https://pastebin.com/api/api_post.php'
CONF = '.py-pastebin.conf'


def _get_home_dir():
    return os.path.expanduser('~')

def _get_config_path():
    conf_path = os.path.join(_get_home_dir(), CONF)
    return conf_path

def login(args):
    if not args.dev_key:
        print("Missing Pasebin API dev key, option [--dev-key|-d]")
        return
    if not args.user:
        print("Missing Pasebin user name, option [--user|-u]")
        return
    if not args.password:
        print("Missing Pasebin user password, option [--password|-p]")
        return

    payload = { 'api_dev_key': args.dev_key,
                'api_user_name': args.user,
                'api_user_password': args.password,
            }
    req_login = requests.post(URL_LOGIN, data=payload)
    if req_login.text.startswith('Bad '):
        print("Login FAILED")
        return
    else:
        print("Login OK")

    config = configparser.ConfigParser()
    config['DEFAULT'] = {
            'api_dev_key': args.dev_key,
            'api_user_name': args.user,
            'api_user_password': args.password,
            'api_user_key': req_login.text}

    with os.fdopen(
            os.open(_get_config_path(),
                    os.O_CREAT|os.O_TRUNC|os.O_WRONLY,
                    0o600), 
            'w') as configfile:
        config.write(configfile)

    return req_login.text

def userdetails():
    payload = { 'api_dev_key': KEY,
                'api_user_key': login(),
                'api_user_name': 'xxxxxxx',
                'api_user_password': 'xxxxxxxx',
                'api_option': 'userdetails',
            }
    req_login = requests.post(URL_LOGIN, data=payload)
    if req_login.text.startswith('Bad '):
        print("FAILED")
    else:
        print("login ok")

def upload(args):
    config = configparser.ConfigParser()
    config.read(_get_config_path())
    api_user_key = config['DEFAULT'].get('api_user_key', None)
    api_dev_key = config['DEFAULT'].get('api_dev_key', None)

    if api_user_key is None or api_dev_key is None:
        print("No existing Pasebin account found, "
              "use [--login, -l] options to login.")
        return

    if args.content:
        content = args.content
    elif args.file:
        print("Reading content from file %s" % args.file)
        with open(args.file, 'r') as f_content:
            content = f_content.read()
    elif args.stdin:
        file_str = StringIO()
        for line in sys.stdin:
            file_str.write(line)
        content = file_str.getvalue()
    else:
        print("Unknown content source")
        return
    if args.verbose:
        print("Paste size: %d" % len(content))

    payload = {
                'api_option': 'paste',
                'api_user_key': api_user_key,
                'api_dev_key': api_dev_key,
                'api_paste_code': content,
                'api_paste_name': args.title,
                'api_paste_private': 1,
                'title': args.title,
                'api_paste_expire_date': args.expiration,
                'api_paste_format': args.format,
              }
    rq = requests.post(URL_PASTE, data=payload)
    print(rq.text)

def main():
    parser = argparse.ArgumentParser(description='Pastebin uploader')
    content_group = parser.add_mutually_exclusive_group(required=True)
    content_group.add_argument('--login', '-l',
            help='Login and create session', action='store_true')
    content_group.add_argument('--file', '-f',
            help='Read content from file')
    content_group.add_argument('--stdin', '-s',
            help='Read content from standard input', action='store_true')
    content_group.add_argument('--content', '-c',
            help='Content specified by this argument')
    parser.add_argument('--title', '-t',
            help='Paste title', default="NoTitle")
    parser.add_argument('--name', '-n',
            help='Paste name', default="NoName")
    parser.add_argument('--expiration', '-e', default='10M',
            help='Paste expire time')
    parser.add_argument('--access', '-a', default=0,
            help='Visability Public/Unlisted/Private, default=[Unlisted]')
    parser.add_argument('--verbose', '-v',
            help='Turn on verbose output', action='store_true')
    parser.add_argument('--format', '-F', help='Paste format')
    parser.add_argument('--user', '-u', help='Pastebin user name')
    parser.add_argument('--password', '-p', help='Pastebin password')
    parser.add_argument('--dev-key', '-d', help='Pastebin API dev key')
    args = parser.parse_args()

    if args.verbose:
        print(args)

    logging.basicConfig()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        HTTPConnection.debuglevel = 0
    else:
        logging.getLogger().setLevel(logging.INFO)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    if args.login:
        login(args)
    else:
        upload(args)


if __name__ == "__main__":
    main()
