import requests
import redis
from functools import wraps
from typing import Callable

# Redis connection
redis_client = redis.Redis()


def cache_expiring(expiration_time: int) -> Callable:
    """
    Decorator to cache the result of a function with an expiration time.

    Args:
        expiration_time: The expiration time in seconds.

    Returns:
        The decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Check if the cached result exists
            cached_result = redis_client.get(url)
            if cached_result:
                return cached_result.decode('utf-8')

            # Call the function and cache the result
            result = func(url)
            redis_client.setex(url, expiration_time, result)
            return result

        return wrapper
    return decorator


@cache_expiring(10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL using requests.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


# Testing the get_page function
if __name__ == '__main__':
    url = 'http://slowwly.robertomurray.co.uk/delay/10000/url/http://example.com'
    content = get_page(url)
    print(content)
