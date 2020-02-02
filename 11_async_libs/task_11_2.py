# -*- coding: utf-8 -*-
"""
Задание 11.2

Создать сопрограмму (coroutine) configure_devices. Сопрограмма
должна настраивать одни и те же команды на указанных устройствах с помощью asyncssh.
Все устройства должны настраиваться параллельно.

Параметры функции:

* devices - список словарей с параметрами подключения к устройствам
* config_commands - команды конфигурационного режима, которые нужно отправить на каждое устройство

Функция возвращает список строк с результатами выполнения команды на каждом устройстве.
Запустить сопрограмму и проверить, что она работает корректно с устройствами
в файле devices.yaml и командами в списке commands.

При необходимости, можно использовать функции из предыдущих заданий
и создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""
from task_11_1 import send_config_commands
import asyncio
import yaml
from pprint import pprint
from itertools import repeat


async def send_command_to_devices(devices, commands):
    coros = map(send_config_commands, devices, repeat(commands))
    return await asyncio.gather(*coros)


if __name__ == "__main__":
    commands = ['router ospf 55',
                'auto-cost reference-bandwidth 1000000',
                'network 0.0.0.0 255.255.255.255 area 0']
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    pprint(devices)
    pprint(asyncio.run(send_command_to_devices(devices, commands)))

