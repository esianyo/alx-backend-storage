#!/usr/bin/env python3
"""
Main file
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


class Cache:
    def __init__(self):
        """
        Cache class to interact with Redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(self, method: Callable) -> Callable:
        """
        Decorator to count the number of times a method is called.
        """
        @wraps(method)
        def wrapper(*args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(*args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key
        and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int, None]:
        """
        Retrieve the data from Redis using the provided key.
        If an optional conversion function (fn) is provided,
        apply the function to convert the data before returning.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve the data from Redis using the provided key
        and convert it to a string before returning.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve the data from Redis using the provided key
        and convert it to an integer before returning.
        """
        return self.get(key, fn=int)

    def replay(self, method: Callable):
        """
        Display the history of calls for a particular method.
        """
        key = method.__qualname__
        calls = self._redis.lrange(key, 0, -1)
        num_calls = len(calls)
        print(f"{key} was called {num_calls} times:")
        for call in calls:
            inputs, output = self._redis.hmget(call, "inputs", "output")
            inputs = eval(inputs)
            print(f"{key}{inputs} -> {output}")


if __name__ == '__main__':
    cache = Cache()

    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    cache.replay(cache.store)
