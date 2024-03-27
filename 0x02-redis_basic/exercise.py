#!/usr/bin/env python3

"""
This module provides a Cache class for storing and retrieving data using Redis.
"""

import redis
import uuid
import functools
from typing import Callable, Optional


class Cache:
    """
    Cache class for storing and retrieving data using Redis.
    """

    def __init__(self):
        """
        Initializes the Cache object and connects to Redis.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data) -> str:
        """
        Stores the given data in Redis and returns the generated key.

        Args:
            data: The data to be stored.

        Returns:
            The generated key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Retrieves the data associated with the given key from Redis.

        Args:
            key: The key to retrieve the data for.
            fn: Optional function to apply to the retrieved data.

        Returns:
            The retrieved data, optionally transformed by the given function.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str):
        """
        Retrieves the string data associated with the given key from Redis.

        Args:
            key: The key to retrieve the data for.

        Returns:
            The retrieved string data.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str):
        """
        Retrieves the integer data associated with the given key from Redis.

        Args:
            key: The key to retrieve the data for.

        Returns:
            The retrieved integer data.
        """
        return self.get(key, fn=lambda x: int(x))

    def count_calls(method):
        """
        Decorator that counts the number of times a method is called.

        Args:
            method: The method to be decorated.

        Returns:
            The decorated method.
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            count_key = f"count:{method.__qualname__}"
            self._redis.incr(count_key)
            return method(self, *args, **kwargs)
        return wrapper

    def call_history(method):
        """
        Decorator that records the inputs and outputs of a method.

        Args:
            method: The method to be decorated.

        Returns:
            The decorated method.
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            inputs_key = f"{method.__qualname__}:inputs"
            outputs_key = f"{method.__qualname__}:outputs"
            self._redis.rpush(inputs_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(outputs_key, output)
            return output
        return wrapper

    @count_calls
    @call_history
    def store(self, data) -> str:
        """
        Stores the given data in Redis, counts the method call,
        and records the history.

        Args:
            data: The data to be stored.

        Returns:
            The generated key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def retrieve_list(self, method_name: str):
        """
        Retrieves the list of inputs and outputs for a method from Redis.

        Args:
            method_name: The name of the method.

        Returns:
            A list of tuples containing the inputs and outputs.
        """
        inputs_key = f"{method_name}:inputs"
        outputs_key = f"{method_name}:outputs"
        inputs = self._redis.lrange(inputs_key, 0, -1)
        outputs = self._redis.lrange(outputs_key, 0, -1)
        return [(input.decode('utf-8'), output.decode('utf-8'))
                for input, output in zip(inputs, outputs)]
