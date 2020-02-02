# Живые - мертвые
# Программа генерирует таблицу из нулей и единиц, либо запрашивает пользователя файл, в котором эта таблица содержится
# обрабатывает ее и выводит новую таблицу каждую секунду
import random as rd
import sys
import copy
import time

pre: float


def gen_desk(m, n):
    """Генерирует доску из m строк и n столбцов"""
    desk = []
    stride = [0]*(n+2)
    desk.append(stride)
    for i in range(m):
        stride = [0]
        for j in range(n):
            stride.append(rd.randrange(0, 2))
        stride.append(0)
        desk.append(stride)
    stride = [0]*(n+2)
    desk.append(stride)
    return desk


def str_to_list(s1):
    """Переводит строку в массив целых чисел"""
    l1 = [0]
    for i in range(len(s1)):
        if s1[i] == '0' or s1[i] == '1':
            l1.append(int(s1[i]))
    l1.append(0)
    return l1


def read_desk_file(name):
    """Читает файл и создает доску из данных файла"""
    desk = []
    try:
        file = open(name, 'r', encoding='utf-8')
        line = file.readline()
        i = 0
        while line != '':
            if ('0' or '1') or ('0' and '1') in line:
                if i == 0:
                    i = len(str_to_list(line))
                    desk.append([0]*i)
                desk.append(str_to_list(line))
            line = file.readline()
        desk.append([0] * i)
    except IOError:
        print('Невозможно открыть файл', name, 'Работа программы будет прекращена\n', 'IOError')
        sys.exit()
    return desk


def sum_around(i, j, desk):
    """Суммирует значения ячеек на доску рядом с ячейкой на поле (i, j)"""
    summary = 0
    for s in range(i-1, i+2, 1):
        for c in range(j-1, j+2, 1):
            if c != j or s != i:
                summary += desk[s][c]
    return summary


def output(desk):
    """Выводит доску в консоль"""
    for i in range(1, len(desk) - 1, 1):
        for j in range(1, len(desk[i]) - 1, 1):
            print(desk[i][j], end='')
        print('\n', end='')
    print('\n\n')


def processing(desk):
    """Изменяет доску, и отправляет её на печать, если прошла секунда"""
    global pre
    desk_check = copy.deepcopy(desk)
    for i in range(1, len(desk) - 1, 1):
        for j in range(1, len(desk[i]) - 1, 1):
            k = sum_around(i, j, desk_check)
            if (k < 2 and desk[i][j] == 1) or (k > 3 and desk[i][j] == 1):
                desk[i][j] = 0
            if k == 3 and desk[i][j] == 0:
                desk[i][j] = 1
            nt = time.time()
            if nt - pre >= 1:
                output(desk)
                print(nt, pre)
                pre = nt
    return desk


def check_equal_desk(desk_1, desk_2):
    """Проверяет доску после обработки с предыдущей доской"""
    i = 1
    while i < len(desk_1) - 1:
        j = 1
        while j < len(desk_1[i]) - 1:
            if desk_1[i][j] != desk_2[i][j]:
                return 1
            else:
                j += 1
        i += 1
    return 0


def get_result(desk):
    """Организует конечно - бесконечный цикл, для изменения доски, критерием выхода из цикла служит равенство досок до и
    после обработки друг другу"""
    global pre
    desk_1 = copy.deepcopy(desk)
    output(desk_1)
    pre = time.time()
    desk_2 = processing(desk)
    while check_equal_desk(desk_1, desk_2) != 0:
        nt = time.time()
        if nt - pre >= 1:
            output(desk_2)
            pre = nt
            desk_1 = copy.deepcopy(desk_2)
            desk_2 = processing(desk_2)
    output(desk_2)


def main():
    sol = input('''введите количество строк и столбцов, через запятую для генерации таблицы
    или имя файла, в котором находится таблица для начала программы:''')
    num = sol.split(',')
    try:
        get_result(gen_desk(int(num[0]), int(num[1])))
    except ValueError:
        get_result(read_desk_file(sol))


main()
