# -*- coding: utf-8 -*-
'''
Задание 19.3

Создать функцию send_commands (для подключения по SSH используется netmiko).

Параметры функции:
* device - словарь с параметрами подключения к устройству, которому надо передать команды
* show - одна команда show (строка)
* config - список с командами, которые надо выполнить в конфигурационном режиме

В зависимости от того, какой аргумент был передан, функция вызывает разные функции внутри.
При вызове функции send_commands, всегда будет передаваться только один из аргументов show, config.

Далее комбинация из аргумента и соответствующей функции:
* show - функция send_show_command из задания 19.1
* config - функция send_config_commands из задания 19.2

Функция возвращает строку с результатами выполнения команд или команды.

Проверить работу функции:
* со списком команд commands
* командой command

Пример работы функции:

In [14]: send_commands(r1, show='sh clock')
Out[14]: '*17:06:12.278 UTC Wed Mar 13 2019'

In [15]: send_commands(r1, config=['username user5 password pass5', 'username user6 password pass6'])
Out[15]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#username user5 password pass5\n
R1(config)#username user6 password pass6\nR1(config)#end\nR1#'
'''
from sys import path
path.append('C:/Python/CHA/ssh_telnet_19/')
from task_19_1b import send_show_command
from task_19_2c import send_config_commands
from yaml import safe_load
from pprint import pprint


def send_commands(device, show=None, config=None):
    if show:
        return send_show_command(device, show)
    else:
        return send_config_commands(device, config)


# don't run on import
if __name__ == '__main__':
    commands = ['logging 10.255.255.1', 'logging buffered 20010', 'no logging console']
    command = 'sh ip int br'
    yaml_of_devices = 'devices.yaml'
    with open(yaml_of_devices) as f:
        templ = safe_load(f)
    for device in templ:
        pprint(send_commands(device, show=command), width=120)
        pprint(send_commands(device, config=commands), width=120)