# -*- coding: utf-8 -*-
"""
YouTube

for more information about selenium, please visit:
https://selenium-python.readthedocs.io/
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import JavascriptException
from modules import utils


class YouTube:
    """ YouTube """
    # pylint: disable=R0904

    def __init__(self, url='https://youtube.com', proxy=None, verbose=False):
        """ init variables """

        self.url = url
        self.proxy = proxy
        self.verbose = verbose
        # All chrome options
        # https://peter.sh/experiments/chromium-command-line-switches/
        self.options = webdriver.ChromeOptions()
        # Run in headless mode, without a UI or display server dependencies
        self.options.add_argument('--headless')
        # Disables GPU hardware acceleration. If software renderer is not in
        # place, then the GPU process won't launch
        self.options.add_argument('--disable-gpu')
        # Disable audio
        self.options.add_argument('--mute-audio')
        # Runs the renderer and plugins in the same process as the browser
        self.options.add_argument('--single-process')
        # Autoplay policy
        self.options.add_argument('--autoplay-policy=no-user-gesture-required')
        if self.proxy:
            # Uses a specified proxy server, overrides system settings. This
            # switch only affects HTTP and HTTPS requests
            self.options.add_argument('--proxy-server={0}'.format(self.proxy))
        # A string used to override the default user agent with a custom one
        self.user_agent = utils.user_agent()
        self.options.add_argument('--user-agent={0}'.format(self.user_agent))
        self.browser = webdriver.Chrome(options=self.options)
        self.default_timeout = 20
        # Specifies the amount of time the driver should wait when trying to
        # find any element (or elements) if it is not immediately available.
        # The default setting is 0. Once set, the implicit wait is set for the
        # life of the WebDriver object.
        self.browser.implicitly_wait(self.default_timeout)
        # Set the amount of time to wait for a page load to complete before
        # throwing an error.
        # self.browser.set_page_load_timeout(self.default_timeout)
        # Set the amount of time that the script should wait during an
        # execute_async_script call before throwing an error.
        # self.browser.set_script_timeout(self.default_timeout)
        # Sets the width and height of the current window$
        self.browser.set_window_size(1920, 1080)
        # Opens the page
        self.open_url()

    def find_by_class(self, class_name):
        """ finds an element by class name """

        # Use this when you want to locate an element by class attribute name.
        # With this strategy, the first element with the matching class
        # attribute name will be returned. If no element has a matching class
        # attribute name, a NoSuchElementException will be raised.

        return self.browser.find_element_by_class_name(class_name)

    def find_all_by_class(self, class_name):
        """ finds all elements by class name """

        return self.browser.find_elements_by_class_name(class_name)

    def find_by_id(self, id_name):
        """ finds a element by id """

        # Use this when you know id attribute of an element. With this
        # strategy, the first element with the id attribute value matching the
        # location will be returned. If no element has a matching id attribute,
        # a NoSuchElementException will be raised.

        return self.browser.find_element_by_id(id_name)

    def find_all_by_id(self, id_name):
        """ finds all elements by id """

        return self.browser.find_elements_by_id(id_name)

    def find_by_name(self, name):
        """ finds a element by name """

        # Use this when you know name attribute of an element. With this
        # strategy, the first element with the name attribute value matching
        # the location will be returned. If no element has a matching name
        # attribute, a NoSuchElementException will be raised.

        return self.browser.find_element_by_name(name)

    def find_all_by_name(self, name):
        """ finds all elements by name """

        return self.browser.find_elements_by_name(name)

    def find_by_xpath(self, xpath):
        """ finds a element by xpath """

        # XPath extends beyond (as well as supporting) the simple methods of
        # locating by id or name attributes, and opens up all sorts of new
        # possibilities such as locating the third checkbox on the page.

        # One of the main reasons for using XPath is when you don’t have a
        # suitable id or name attribute for the element you wish to locate.
        # You can use XPath to either locate the element in absolute terms
        # (not advised), or relative to an element that does have an id or
        # name attribute. XPath locators can also be used to specify elements
        # via attributes other than id and name.

        # Absolute XPaths contain the location of all elements from the root
        # (html) and as a result are likely to fail with only the slightest
        # adjustment to the application. By finding a nearby element with an
        # id or name attribute (ideally a parent element) you can locate your
        # target element based on the relationship. This is much less likely
        # to change and can make your tests more robust.

        return self.browser.find_element_by_xpath(xpath)

    def find_all_by_xpath(self, xpath):
        """ finds all elements by xpath """

        return self.browser.find_elements_by_xpath(xpath)

    def click(self, how, what):
        """ clicks on the element """

        try:
            wait = WebDriverWait(self.browser, self.default_timeout)
            wait.until(EC.element_to_be_clickable((how, what))).click()
        except (ElementClickInterceptedException, TimeoutException):
            return False
        return True

    def open_url(self):
        """ opens the URL """

        self.browser.get(self.url)

    def get_current_url(self):
        """ gets the current url """

        return self.browser.current_url

    def get_title(self, id_name='video-title'):
        """ gets the video title """

        # waits up to 10 seconds before throwing a TimeoutException unless it
        # finds the element to return within 10 seconds. WebDriverWait by
        # default calls the ExpectedCondition every 500 milliseconds until it
        # returns successfully. A successful return is for ExpectedCondition
        # type is Boolean return true or not null return value for all other
        # ExpectedCondition types.

        try:
            wait = WebDriverWait(self.browser, self.default_timeout)
            wait.until(EC.presence_of_element_located((By.ID, id_name)))
            return self.browser.title
        except TimeoutException:
            return None

    def search(self, query):
        """ searches for the given term(s) and print the result """

        result = {}
        try:
            search = self.find_by_name('search_query')
            time.sleep(2)
            search.click()
            time.sleep(2)
            search.clear()
            search.send_keys(query)
            time.sleep(10)
            search.send_keys(Keys.DOWN)
            search.send_keys(Keys.ENTER)
            self.click(
                By.XPATH,
                "//div[@id='more']/yt-formatted-string/span[3]")
            wait = WebDriverWait(self.browser, self.default_timeout)
            wait.until(
                EC.visibility_of_all_elements_located(
                    ((By.CSS_SELECTOR,
                      'a.yt-simple-endpoint.style-scope.ytd-video-renderer#video-title'))))
            items = self.find_all_by_xpath(
                '//*[@id="contents"]/ytd-video-renderer')
            for item in items:
                if item.is_displayed():
                    v_info = item.find_element_by_id('video-title')
                    c_info = item.find_element_by_class_name(
                        'ytd-channel-name')
                    v_link = v_info.get_attribute('href')
                    v_id = v_link.strip('https://www.youtube.com/watch?v=')
                    v_title = v_info.get_attribute('title')
                    c_url = c_info.find_element_by_class_name(
                        'yt-formatted-string').get_attribute('href')
                    result[v_id] = {
                        'id': v_id,
                        'video title': v_title,
                        'video url': v_link,
                        'channel name': c_info.text,
                        'channel url': c_url,
                        'element': v_info,
                    }
            return result
        except NoSuchElementException:
            return None

    def play_video(self, class_name='ytp-play-button'):
        """ clicks on the play button """

        self.click(By.CLASS_NAME, class_name)

    def mute_video(self, class_name='ytp-mute-button'):
        """ clicks on the mute button """

        self.click(By.CLASS_NAME, class_name)

    def skip_ad(self, class_name='ytp-ad-skip-button-text', max_attempts=20, time_wait=0.5):
        """ skips ads """

        attempts = 0
        while attempts <= max_attempts:
            try:
                button = self.find_by_class(class_name)
                if button.is_enabled() or button.is_displayed():
                    if self.verbose:
                        print(button.get_attribute('textContent').lower())
                    button.click()
            except (ElementNotInteractableException, ElementClickInterceptedException):
                time.sleep(time_wait)
            except (NoSuchElementException, TimeoutException, AttributeError):
                break
            attempts += 1

    def get_views(self, class_name='view-count'):
        """ gets the total views """

        try:
            views = self.find_by_class(class_name).get_attribute('textContent')
            return views.strip(' views')
        except NoSuchElementException:
            return None

    def get_channel_name(self, class_name='ytd-channel-name'):
        """ gets the channel name """

        try:
            return self.find_by_class(class_name).text
        except NoSuchElementException:
            return None

    def get_subscribers(self, id_name='owner-sub-count'):
        """ gets the total of subscribers """

        try:
            return self.find_by_id(id_name).text.strip(' subscribers')
        except NoSuchElementException:
            return None

    def get_player_state(self):
        """  returns the state of the player """

        # Possible values are:
        # -1 = unstarted
        #  0 = ended
        #  1 = playing
        #  2 = paused
        #  3 = buffering
        #  5 = video cued
        # for more information, you can check the official API documentation:
        # https://developers.google.com/youtube/iframe_api_reference

        try:
            js_element = "return document.getElementById('movie_player').getPlayerState()"
            return self.browser.execute_script(js_element)
        except JavascriptException:
            return -2

    def refresh_page(self):
        """ refreshes the page """

        self.browser.refresh()

    def time_duration(self, class_name='ytp-time-duration'):
        """ gets the video duration time """

        try:
            duration = self.find_by_class(class_name)
            if duration:
                return duration.get_attribute('textContent')
        except NoSuchElementException:
            return None
        return None

    def disconnect(self):
        """ closes the connection """

        self.browser.close()
        self.browser.quit()

# vim: set et ts=4 sw=4 sts=4 tw=80


def is_valid_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


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


def get_env(key: str, default: str = '') -> str:
    import os
    return os.environ.get(key, default)


def deep_get(d: dict, *keys, default=None):
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, default)
    return d


def flatten(nested: list) -> list:
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def human_size(n_bytes: int) -> str:
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n_bytes < 1024:
            return f'{n_bytes:.1f} {unit}'
        n_bytes /= 1024
    return f'{n_bytes:.1f} PB'


def read_json(path: str) -> dict:
    import json
    from pathlib import Path
    return json.loads(Path(path).read_text(encoding='utf-8'))


def batch(iterable, n: int):
    from itertools import islice
    it = iter(iterable)
    while chunk := list(islice(it, n)):
        yield chunk


def chunk_list(lst: list, size: int):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def is_palindrome(s: str) -> bool:
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def read_json(path: str) -> dict:
    import json
    from pathlib import Path
    return json.loads(Path(path).read_text(encoding='utf-8'))


def read_json(path: str) -> dict:
    import json
    from pathlib import Path
    return json.loads(Path(path).read_text(encoding='utf-8'))


def unique_preserve_order(seq: list) -> list:
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


def get_env(key: str, default: str = '') -> str:
    import os
    return os.environ.get(key, default)


def read_json(path: str) -> dict:
    import json
    from pathlib import Path
    return json.loads(Path(path).read_text(encoding='utf-8'))


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
