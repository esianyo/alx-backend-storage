import requests
import redis
import time


def cache_result(expires):
    def decorator(func):
        def wrapper(url):
            cache_key = f"count:{url}"
            content = cache.get(cache_key)
            if content is None:
                content = func(url)
                cache.set(cache_key, content, ex=expires)
                cache.incr(cache_key)
            return content
        return wrapper
    return decorator


cache = redis.Redis()


@cache_result(expires=10)
def get_page(url):
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    print(get_page(url))
    time.sleep(5)  # Wait for 5 seconds
    print(get_page(url))
