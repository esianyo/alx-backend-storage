import requests
import time
from functools import wraps


CACHE = {}


def cache_expiration(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            if url in CACHE:
                if time.time() - CACHE[url]['timestamp'] < seconds:
                    CACHE[url]['count'] += 1
                    return CACHE[url]['content']

            content = func(url)
            CACHE[url] = {'content': content,
                          'timestamp': time.time(), 'count': 1}
            return content
        return wrapper
    return decorator


@cache_expiration(10)
def get_page(url):
    response = requests.get(url)
    return response.text
