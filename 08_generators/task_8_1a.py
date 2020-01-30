# -*- coding: utf-8 -*-
"""
Задание 8.1a

Создать генератор get_intf_ip, который ожидает как аргумент имя файла,
в котором находится конфигурация устройства и возвращает все интерфейсы и IP-адреса,
которые настроены на интерфейсах.

Генератор должен обрабатывать конфигурацию и возвращать кортеж на каждой итерации:
* первый элемент кортежа - имя интерфейса
* второй элемент кортежа - IP-адрес
* третий элемент кортежа - маска

Например: ('FastEthernet', '10.0.1.1', '255.255.255.0')

Проверить работу генератора на примере файла config_r1.txt.
"""
import re


def get_intf_ip(filename):
    with open(filename) as f:
        for line in f:
            match = re.match('interface (\S+)', line)
            if match:
                interface = match.group(1)
            else:
                match = re.match(' ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    yield interface, match.group(1), match.group(2)


# don't run on import
if __name__ == "__main__":
    for n in get_intf_ip('config_r1.txt'):
        print(n)