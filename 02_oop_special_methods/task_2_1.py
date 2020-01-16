# -*- coding: utf-8 -*-
'''
Задание 2.1

Скопировать класс IPv4Network из задания 1.1 и добавить ему все методы,
которые необходимы для реализации протокола последовательности (sequence):
* __getitem__, __len__, __contains__, __iter__
* index, count - должны работать аналогично методам в списках и кортежах

И оба метода, которые отвечают за строковое представление экземпляров
класса IPv4Network.

Существующие методы и атрибуты (из задания 1.1) можно менять, при необходимости.

Пример создания экземпляра класса:

In [2]: net1 = IPv4Network('8.8.4.0/29')

Проверка методов:

In [3]: for ip in net1:
   ...:     print(ip)
   ...:
8.8.4.1
8.8.4.2
8.8.4.3
8.8.4.4
8.8.4.5
8.8.4.6

In [4]: net1[2]
Out[4]: '8.8.4.3'

In [5]: net1[-1]
Out[5]: '8.8.4.6'

In [6]: net1[1:4]
Out[6]: ('8.8.4.2', '8.8.4.3', '8.8.4.4')

In [7]: '8.8.4.4' in net1
Out[7]: True

In [8]: net1.index('8.8.4.4')
Out[8]: 3

In [9]: net1.count('8.8.4.4')
Out[9]: 1

In [10]: len(net1)
Out[10]: 6

Строковое представление:

In [13]: net1
Out[13]: IPv4Network(8.8.4.0/29)

In [14]: str(net1)
Out[14]: 'IPv4Network 8.8.4.0/29'

'''
from task_1_1 import IPv4Network


#don't run on import
if __name__ == "__main__":
    net1 = IPv4Network('8.8.4.0/29')
    print(net1)
    print([net1])
    print('*'*45)
    print(len(net1))
    print('*'*45)
    print(net1[2])
    print(net1[-1])
    print(net1[1:4])
    print('*'*45)
    for ip in net1:
        print(ip)
    print('*'*45)
    print(net1.index('8.8.4.4'))
    print(net1.count('8.8.4.4'))
    print('*'*45)
    print('8.8.4.4' in net1)