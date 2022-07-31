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


def count_words(text: str) -> int:
    return len(text.split())


def count_words(text: str) -> int:
    return len(text.split())


def is_valid_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def get_env(key: str, default: str = '') -> str:
    import os
    return os.environ.get(key, default)


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


def count_words(text: str) -> int:
    return len(text.split())


def write_json(path: str, data: dict, indent: int = 2) -> None:
    import json
    from pathlib import Path
    Path(path).write_text(json.dumps(data, indent=indent, ensure_ascii=False))


def get_env(key: str, default: str = '') -> str:
    import os
    return os.environ.get(key, default)


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def color_hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def zip_dicts(*dicts: dict) -> dict:
    result = {}
    for d in dicts:
        result.update(d)
    return result


def chunk_list(lst: list, size: int):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def read_json(path: str) -> dict:
    import json
    from pathlib import Path
    return json.loads(Path(path).read_text(encoding='utf-8'))


def deep_merge(base: dict, override: dict) -> dict:
    out = base.copy()
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def batch(iterable, n: int):
    from itertools import islice
    it = iter(iterable)
    while chunk := list(islice(it, n)):
        yield chunk


def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in ('1', 'true', 'yes', 'on')


def zip_dicts(*dicts: dict) -> dict:
    result = {}
    for d in dicts:
        result.update(d)
    return result
