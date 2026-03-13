# -*- coding: utf-8 -*-
"""
This module provides utility functions that are used within youtube.py that
are also useful for external consumption
"""

import sys
import json
import argparse
from random import choice
from datetime import timedelta
import socket
import time
import requests


def user_agent():
    """ returns a random user agent """

    # All user agents
    # https://www.whatismybrowser.com/guides/the-latest-user-agent/

    user_agents = {
        'edge_on_windows': [
            'Mozilla/5.0',
            '(Windows NT 10.0; Win64; x64)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36 Edg/79.0.309.71',
        ],
        'safari_on_mac': [
            'Mozilla/5.0',
            '(Macintosh; Intel Mac OS X 10_13_6)',
            'AppleWebKit/605.1.15',
            '(KHTML, like Gecko)',
            'Version/13.0 Safari/605.1.15',
        ],
        'chrome_on_windows': [
            'Mozilla/5.0',
            '(Windows NT 10.0; Win64; x64)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36',
        ],
        'chrome_on_mac': [
            'Mozilla/5.0',
            '(Macintosh; Intel Mac OS X 10_15_2)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36',
        ],
        'chrome_on_linux': [
            'Mozilla/5.0',
            '(X11; Linux x86_64)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36',
        ],
        'firefox_on_windows': [
            'Mozilla/5.0',
            '(Windows NT 10.0; WOW64; rv:50.0)',
            'Gecko/20100101 Firefox/72.0',
        ],
        'firefox_on_mac': [
            'Mozilla/5.0',
            '(Macintosh; Intel Mac OS X 10.15; rv:72.0)',
            'Gecko/20100101 Firefox/72.0',
        ],
        'firefox_on_linux': [
            'Mozilla/5.0',
            '(X11; Linux x86_64; rv:72.0)',
            'Gecko/20100101 Firefox/72.0',
        ],
    }
    values = [value for key, value in user_agents.items()]
    return ' '.join(choice(values))


def to_seconds(duration='0:02'):
    """ converts h:m:s to seconds """

    if isinstance(duration, str):
        duration = duration.split(':')
    _hour, _min, _sec = (0, 0, 0)
    if len(duration) == 3:
        _hour, _min, _sec = duration
    elif len(duration) == 2:
        _min, _sec = duration

    _seconds = timedelta(
        hours=int(_hour),
        minutes=int(_min),
        seconds=int(_sec))
    return int(_seconds.total_seconds())


def get_ipaddr(url='http://httpbin.org/ip', proxy=None):
    """ gets the external IP address """

    if proxy:
        proxy = 'http://{0}'.format(proxy)
        proxies = {'http': proxy, 'https': proxy}
        response = requests.get(url, proxies=proxies)
    else:
        response = requests.get(url)

    if response.status_code == 200:
        try:
            return json.loads(response.content.decode('utf-8'))['origin']
        except json.decoder.JSONDecodeError:
            return None
    return None


def get_host_by_ipaddr(ipaddr):
    """ returns a reverse DNS name if available """

    try:
        socket.inet_aton(ipaddr)
        return socket.gethostbyaddr(ipaddr)[0]
    except socket.herror:
        return 'no reverse DNS found'
    except (socket.error, TypeError):
        return 'illegal IP address string'
    except socket.timeout:
        return 'DNS timeout'


def renew_tor_ipaddr(ipaddr='127.0.0.1', port=9051, password=None, time_wait=0.2, verbose=False):
    """ connects to TOR and request a new IP address """

    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((ipaddr, int(port)))
        time.sleep(time_wait)
        if password:
            conn.send('AUTHENTICATE "{0}"\r\n'.format(password).encode())
        else:
            conn.send('AUTHENTICATE\r\n'.encode())
        auth_response = conn.recv(128).decode()
        time.sleep(time_wait)
        if 'OK' in auth_response:
            if verbose:
                print('tor: authentication success')
                print('tor: requesting new IP address')
            conn.send('SIGNAL NEWNYM\r\n'.encode())
            signal_response = conn.recv(128).decode()
            if 'OK' in signal_response and verbose:
                print('tor: new IP address requested successfully')
        elif 'failed' in auth_response:
            print('tor: authentication failed')
            conn.close()
        time.sleep(time_wait)
        conn.send('QUIT\r\n'.encode())
        # conn_response = conn.recv(128).decode()
        conn.close()
    except (socket.error, socket.timeout, ConnectionRefusedError, OverflowError):
        return False
    return True


def get_new_tor_ipaddr(password=None, proxy=None, max_attempts=10, time_wait=5):
    """ gets a new Tor IP address """

    attempts = 0
    current_ipaddr, new_ipaddr = None, None

    while current_ipaddr == new_ipaddr:
        current_ipaddr = get_ipaddr(proxy=proxy)
        if proxy:
            renew_tor_ipaddr(ipaddr=proxy.split(':')[0], password=password)
        else:
            renew_tor_ipaddr(password=password)
        time.sleep(time_wait)
        new_ipaddr = get_ipaddr(proxy=proxy)
        if attempts == max_attempts:
            print('failed to get a new Tor IP address')
            return None
        attempts += 1
    return new_ipaddr


def get_cli_args():
    """ gets command line arguments """

    parser = argparse.ArgumentParser(
        description='Tool to increase YouTube views',
        add_help=False,
    )

    # main arguments
    main = parser.add_argument_group(
        'Main Arguments',
    )
    main.add_argument(
        '--visits',
        type=int,
        default=1,
        help='amount of times the video will be viewed. Default: 1',
    )
    main.add_argument(
        '--url',
        help='YouTube video url',
    )
    main.add_argument(
        '--proxy',
        help='set the proxy server to be used. e.g: 127.0.0.1:8118',
    )
    main.add_argument(
        '--enable-tor',
        action='store_true',
        help='enable TOR support (You must have installed TOR at your system)',
    )
    # optional arguments
    optional = parser.add_argument_group('Optional Arguments')
    optional.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='show more output',
    )
    optional.add_argument(
        '-h', '--help',
        action='store_true',
        help='show this help message and exit',
    )

    args = parser.parse_args()
    if len(sys.argv) == 1 or args.help:
        parser.print_help()
        sys.exit(0)
    if args.enable_tor is True and args.proxy is None:
        parser.error('--enable-tor requires --proxy')
        sys.exit(0)

    return args


# vim: set et ts=4 sw=4 sts=4 tw=80


def flatten(nested: list) -> list:
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def timer(fn):
    import time, functools
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        print(f'{fn.__name__} took {elapsed:.4f}s')
        return result
    return wrapper


def format_currency(amount: float, symbol: str = '$') -> str:
    return f'{symbol}{amount:,.2f}'


def snake_to_camel(name: str) -> str:
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def format_currency(amount: float, symbol: str = '$') -> str:
    return f'{symbol}{amount:,.2f}'


def zip_dicts(*dicts: dict) -> dict:
    result = {}
    for d in dicts:
        result.update(d)
    return result


def deep_merge(base: dict, override: dict) -> dict:
    out = base.copy()
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def zip_dicts(*dicts: dict) -> dict:
    result = {}
    for d in dicts:
        result.update(d)
    return result


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def deep_get(d: dict, *keys, default=None):
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, default)
    return d


def remove_duplicates(lst: list) -> list:
    return list(dict.fromkeys(lst))


def chunk_list(lst: list, size: int):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in ('1', 'true', 'yes', 'on')


def human_size(n_bytes: int) -> str:
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n_bytes < 1024:
            return f'{n_bytes:.1f} {unit}'
        n_bytes /= 1024
    return f'{n_bytes:.1f} PB'


def is_palindrome(s: str) -> bool:
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def count_words(text: str) -> int:
    return len(text.split())


def zip_dicts(*dicts: dict) -> dict:
    result = {}
    for d in dicts:
        result.update(d)
    return result


def unique_preserve_order(seq: list) -> list:
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


def truncate(text: str, length: int = 100, suffix: str = '...') -> str:
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def safe_divide(a, b, default=0):
    return a / b if b != 0 else default


def slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[\s_-]+', '-', text)


def get_env(key: str, default: str = '') -> str:
    import os
    return os.environ.get(key, default)


def chunk_list(lst: list, size: int):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def deep_get(d: dict, *keys, default=None):
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, default)
    return d

// [2026-04-01 09:00:00]
// update

// [2026-04-20 10:17:00]
// update

// [2026-04-20 11:34:00]
// update

// [2026-05-23 09:00:00]
// update

// [2026-06-18 09:00:00]
// update

// [2026-07-12 10:17:00]
// update

// [2026-07-18 11:34:00]
// update

// [2026-02-04 09:00:00]
// update

// [2026-05-28 11:34:00]
// update

// [2026-06-19 09:00:00]
// update

// [2026-06-26 10:17:00]
// update

// [2026-03-13 09:00:00]
// update

// [2026-03-13 10:17:00]
// update
