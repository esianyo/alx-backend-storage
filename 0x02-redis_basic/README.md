# 0x02. Redis Basic

## Description
This project focuses on utilizing Redis, a powerful data structure server, for basic operations and as a simple cache in a Python-based back-end application.

## Installation
Before running the files in this project, ensure that you have Redis installed on your system. Follow the steps below to install Redis on Ubuntu 18.04:

1. Open a terminal.
2. Run the following command to install Redis server:
   ```
   $ sudo apt-get -y install redis-server
   ```
3. Install the Redis Python client by running:
   ```
   $ pip3 install redis
   ```
4. Configure Redis to bind to localhost (127.0.0.1):
   ```
   $ sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
   ```
   This ensures that Redis only listens for connections on the local interface.

## Usage
To use Redis in a container, please follow the steps below:

1. Start the Redis server within the container:
   ```
   $ service redis-server start
   ```
   This command starts the Redis server, allowing you to interact with it.

## Repository Structure
The repository contains the following files:

- `file_name.py`: Description of the file's purpose.

## Requirements
- Ubuntu 18.04 LTS
- Python 3.7
- pycodestyle 2.5
- Redis server
- Redis Python client

## Style Guide
Ensure that your code follows the pycodestyle style (version 2.5) to maintain consistency and readability.

## Documentation
All modules, classes, functions, and methods should include proper documentation. The length of the documentation should be sufficient to provide a clear understanding of the purpose and functionality of the respective code entity.

To access the documentation for a module, class, function, or method, use the following commands:

- Module: `python3 -c 'print(__import__("my_module").__doc__)'`
- Class: `python3 -c 'print(__import__("my_module").MyClass.__doc__)'`
- Function/Method: `python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`

## Type Annotations
All functions and coroutines must be type-annotated to provide clarity about the expected input and return types.

## Credits
- [Redis Crash Course Tutorial](https://redis.io/topics/data-types-intro)
- [Redis commands](https://redis.io/commands)
- [Redis Python client](https://redis-py.readthedocs.io/en/stable/)
- [How to Use Redis With Python](https://realpython.com/python-redis/)