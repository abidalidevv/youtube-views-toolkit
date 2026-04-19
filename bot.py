#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" Bot to increase YouTube views """

import sys
import time
from random import randrange
from modules.youtube import YouTube
from modules import utils


class Bot:
    """ A bot to increase YouTube views """
    # pylint: disable=R0903,R0912

    def __init__(self, options):
        """ init variables """

        self.opts = options

    @staticmethod
    def player_status(value):
        """ returns the status based one the input code """

        status = {
            -1: 'unstarted',
            0: 'ended',
            1: 'playing',
            2: 'paused',
            3: 'buffering',
            5: 'video cued',
        }
        return status[value] if value in status else 'unknown'

    def run(self):
        """ run """

        count = 1
        ipaddr = None
        while count <= self.opts.visits:
            if self.opts.enable_tor:
                ipaddr = utils.get_new_tor_ipaddr(proxy=self.opts.proxy)
            if not ipaddr:
                ipaddr = utils.get_ipaddr(proxy=self.opts.proxy)
            youtube = YouTube(
                url=self.opts.url,
                proxy=self.opts.proxy,
                verbose=self.opts.verbose
            )
            title = youtube.get_title()
            if not title:
                if self.opts.verbose:
                    print('there was a problem loading this page. Retrying...')
                    youtube.disconnect()
                    continue
            if self.opts.visits:
                length = (len(title) + 4 - len(str(count)))
                print('[{0}] {1}'.format(count, '-' * length))
            if ipaddr:
                print('external IP address:', ipaddr)
            channel_name = youtube.get_channel_name()
            if channel_name:
                print('channel name:', channel_name)
            subscribers = youtube.get_subscribers()
            if subscribers:
                print('subscribers:', subscribers)
            print('title:', title)
            views = youtube.get_views()
            if views:
                print('views:', views)
            # youtube.play_video()
            youtube.skip_ad()
            if self.opts.verbose:
                status = youtube.get_player_state()
                print('video status:', self.player_status(status))
            video_duration = youtube.time_duration()
            seconds = 30
            if video_duration:
                print('video duration time:', video_duration)
                seconds = utils.to_seconds(duration=video_duration.split(':'))
                if seconds:
                    if self.opts.verbose:
                        print('video duration time in seconds:', seconds)
            sleep_time = randrange(seconds)
            print('stopping video in %s seconds' % sleep_time)
            time.sleep(sleep_time)
            youtube.disconnect()
            count += 1


def _main():
    """ main """

    try:
        cli_args = utils.get_cli_args()
        bot = Bot(cli_args)
        bot.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    sys.exit(_main())

# vim: set et ts=4 sw=4 sts=4 tw=80


def read_json(path: str) -> dict:
    import json
    from pathlib import Path
    return json.loads(Path(path).read_text(encoding='utf-8'))


def snake_to_camel(name: str) -> str:
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def get_env(key: str, default: str = '') -> str:
    import os
    return os.environ.get(key, default)


def flatten(nested: list) -> list:
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def levenshtein(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if not s2:
        return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j + 1] + 1, curr[-1] + 1, prev[j] + (c1 != c2)))
        prev = curr
    return prev[-1]


def zip_dicts(*dicts: dict) -> dict:
    result = {}
    for d in dicts:
        result.update(d)
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


def zip_dicts(*dicts: dict) -> dict:
    result = {}
    for d in dicts:
        result.update(d)
    return result


def batch(iterable, n: int):
    from itertools import islice
    it = iter(iterable)
    while chunk := list(islice(it, n)):
        yield chunk


def snake_to_camel(name: str) -> str:
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def truncate(text: str, length: int = 100, suffix: str = '...') -> str:
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def chunk_list(lst: list, size: int):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def paginate(items: list, page: int, per_page: int) -> dict:
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        'items': items[start:end],
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page,
    }


def format_currency(amount: float, symbol: str = '$') -> str:
    return f'{symbol}{amount:,.2f}'


def remove_duplicates(lst: list) -> list:
    return list(dict.fromkeys(lst))


def is_palindrome(s: str) -> bool:
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def camel_to_snake(name: str) -> str:
    import re
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def truncate(text: str, length: int = 100, suffix: str = '...') -> str:
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def write_json(path: str, data: dict, indent: int = 2) -> None:
    import json
    from pathlib import Path
    Path(path).write_text(json.dumps(data, indent=indent, ensure_ascii=False))


def batch(iterable, n: int):
    from itertools import islice
    it = iter(iterable)
    while chunk := list(islice(it, n)):
        yield chunk


def format_currency(amount: float, symbol: str = '$') -> str:
    return f'{symbol}{amount:,.2f}'


def memoize(fn):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def memoize(fn):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper


def camel_to_snake(name: str) -> str:
    import re
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def memoize(fn):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper


def human_size(n_bytes: int) -> str:
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n_bytes < 1024:
            return f'{n_bytes:.1f} {unit}'
        n_bytes /= 1024
    return f'{n_bytes:.1f} PB'


def remove_duplicates(lst: list) -> list:
    return list(dict.fromkeys(lst))


def unique_preserve_order(seq: list) -> list:
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]

// [2026-02-20 09:00:00]
// update

// [2026-04-01 10:17:00]
// update

// [2026-05-23 10:17:00]
// update

// [2026-07-18 09:00:00]
// update

// [2026-07-18 10:17:00]
// update

// [2026-05-28 09:00:00]
// update

// [2026-06-26 09:00:00]
// update

// [2026-06-26 11:34:00]
// update

// [2026-01-20 09:00:00]
// update

// [2026-04-19 09:00:00]
// update

// [2026-04-19 10:17:00]
// update
