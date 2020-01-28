# -*- coding: utf-8 -*-
'''
Задание 6.2

Создать функцию count_total, которая вычисляет сумму потраченную на категорию товаров.
После вызова функции count_total, должна возвращаться внутренняя функция.
При вызове внутренней функции надо передавать аргумент - число.
Как результат должна возвращаться текущая сумма чисел.

Пример использования функции count_total:

In [2]: books = count_total()

In [3]: books(25)
Out[3]: 25

In [4]: books(15)
Out[4]: 40

In [5]: books(115)
Out[5]: 155

In [6]: books(25)
Out[6]: 180

In [7]: toys = count_total()

In [8]: toys(67)
Out[8]: 67

In [9]: toys(17)
Out[9]: 84

In [10]: toys(24)
Out[10]: 108
'''
def count_total():
    sum = 0
    def total(num):
        nonlocal sum
        sum += num
        return sum
    return total
    

# don't run on import
if __name__ == "__main__":
    books = count_total()
    print(books(25))
    print(books(15))
    print(books(115))
    toys = count_total()
    print(toys(25))
    print(toys(15))
    print(toys(115))
