# -*- coding: utf-8 -*-
"""
Задание 12.6

Создать декоратор для сопрограмм retry, который выполняет декорируемую сопрограмму повторно,
заданное количество раз, если результат функции не был истинным.

Пример работы декоратора:
In [2]: @retry(times=3)
    ..: async def connect_ssh(device, command):
    ..:     print(f'Подключаюсь к {device["host"]}')
    ..:     try:
    ..:         async with netdev.create(**device) as ssh:
    ..:             output = await ssh.send_command(command)
    ..:         return output
    ..:     except netdev.DisconnectError:
    ..:         return None


In [3]: connect_ssh(device_params, 'sh clock')
Подключаюсь к 192.168.100.1
Out[3]: '*19:55:59.309 UTC Mon Nov 11 2019'


In [4]: device_params['password'] = '123123'

Обратите внимание, что если указано, что повторить попытку надо 3 раза,
то это три раза в дополнение к первому, то есть все подключение будет 4 раза:
In [5]: connect_ssh(device_params, 'sh clock')
Подключаюсь к 192.168.100.1
Подключаюсь к 192.168.100.1
Подключаюсь к 192.168.100.1
Подключаюсь к 192.168.100.1

Проверить работу декоратора на сопрограмме connect_ssh.

На каждой итерации должен проверяться результат функции. То есть не просто
повторяем вызов функции n раз, а каждый раз проверяем его и необходимость повторения.
"""

import asyncio
import netdev
from functools import wraps


def retry(func=None, times=1):
    if not func:
        return lambda fun: retry(fun, times=times)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        for _ in range(times + 1):
            result = await func(*args, **kwargs)
            if result:
                return result

    return wrapper


@retry(times=3)
async def connect_ssh(device, command):
    print(f'Подключаюсь к {device["host"]}')
    try:
        async with netdev.create(**device) as ssh:
            output = await ssh.send_command(command)
        return output
    except (netdev.DisconnectError, netdev.exceptions.TimeoutError):
        return None


if __name__ == "__main__":
    device_params = {
        'device_type': 'cisco_ios',
        'host': '10.111.111.11',
        'username': 'admin',
        'password': 'cisco',
        'secret': 'cisco'
    }
    # device_params['password'] = '123123'
    print(asyncio.run(connect_ssh(device_params, 'sh clock')))
