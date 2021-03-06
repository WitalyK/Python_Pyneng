# -*- coding: utf-8 -*-
'''
Задание 3.1a

Скопировать класс IPv4Network из задания 3.1.
Добавить метод from_tuple, который позволяет создать экземпляр класса IPv4Network
из кортежа вида ('10.1.1.0', 29).

Пример создания экземпляра класса:

In [3]: net2 = IPv4Network.from_tuple(('10.1.1.0', 29))

In [4]: net2
Out[4]: IPv4Network(10.1.1.0/29)

'''
from task_3_1 import IPv4Network


#don't run on import
if __name__ == "__main__":
    net2 = IPv4Network.from_tuple(('10.1.1.0', 29))
    print([net2])