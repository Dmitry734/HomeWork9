import os
import math
import string
from random import Random, randint

# ==========================================================================================================
# FUNCTIONS
# ==========================================================================================================


def show_desc(List):
    for item in List:
        flor = "["
        for x in item:
            flor += x+" "
        flor = flor[0:-1]
        flor += "]"
        print(f'{flor}')
    print()


def CheckInSumm(mode, List):  # Проверка набора суммы (для Проверка победы), формирование ответа
    oconchanie = ''
    if mode == 'строки':
        oconchanie = '-й'
    elif mode == 'столбца':
        oconchanie = '-го'
    elif mode != 'диагонали':
        oconchanie = '-ой'

    for i in range(len(List)):
        if List[i] == 3 or List[i] == -3:
            return "Выйгрыш: заполнение "+str(i+1)+oconchanie+" " + mode
    return ''


def CheckIn(List):  # Проверка победы
    # +++(0) Инициализация
    i = 0
    SummList = [0, 0, 0]
    # ---(0) Инициализация
    # +++(1) Проверка победы в строках
    for item in List:
        for x in item:
            SummList[i] += x
        i += 1
    text = CheckInSumm('строки', SummList)
    if text != '':
        return text
    # ---(1) Проверка победы в строках
    # +++(2) Проверка победы в столбцах
    SummList = [0, 0, 0]
    for j in range(0, 3):
        for i in range(0, 3):
            SummList[j] += List[i][j]
    text = CheckInSumm('столбца', SummList)
    if text != '':
        return text
    # ---(2) Проверка победы в столбцах
    # +++(3) Проверка победы в диагонали
    SummList = [0, 0, 0]
    for j in range(0, 3):
        SummList[0] += List[j][j]
    for j in range(2, -1, -1):
        i = abs(j-2)
        SummList[1] += List[i][j]
    text = CheckInSumm('диагонали', SummList)
    if text != '':
        return text
    # ---(3) Проверка победы в диагонали
    return ''


def CheckCoordinates(List):
    counter = 0
    if len(List) > 2:
        return "Вы ввели более 2 цифр, координата состоят из 2 цифр, попробуйте еще раз"
    if len(List) < 2:
        return "Вы ввели менее 2 цифр, координата состоят из 2 цифр, попробуйте еще раз"
    for item in List:
        if item.isdigit():
            if int(item) > 0 and int(item) < 4:
                counter += 1
        else:
            return "Неверно! Не все из введенного является натуральными числами, попробуйте еще раз"
    if counter == 2:
        return ''
    return 'Вы не соблюдаете условия, введенные числа должны быть от 1 до 3-х, попробуйте еще раз'


# Алгоритм нахождения координат для бота текущей ситуации для выбора лучшего решения
def WhereToInput(AdressList, List):
    ReturnList = [0, 0]
    # AdressList - это список с указанием номера строки/столбца/диагонали где наименьшее значение и обозначение, куда ставить следующи выбор:строка/столбец/диагональ
    # строка =0 столбец=1 диагональ=2
    # List - это общий список игры, где бот выставляет только -1, а игрок только +1
    if AdressList[1] == 0:  # строка =0
        for j in range(len(List[AdressList[0]])):
            if List[AdressList[0]][j] != -1:
                # Поиск первой подходящей коорднаты
                ReturnList[0] = AdressList[0]
                ReturnList[1] = j
    elif AdressList[1] == 1:  # столбец=1
        for i in range(len(List[AdressList[0]])):
            if List[i][AdressList[0]] != -1:
                # Поиск первой подходящей коорднаты
                ReturnList[0] = i
                ReturnList[1] = AdressList[0]
    elif AdressList[1] == 2:  # диагональ=2
        if AdressList[0] == 0:  # Первая диагональ
            for i in range(0, 3):
                if List[i][i] != -1:
                    # Поиск первой подходящей коорднаты
                    ReturnList[0] = i
                    ReturnList[1] = i
        elif AdressList[0] == 1:  # Вторая диагональ
            for j in range(2, -1, -1):
                i = abs(j-2)
                if List[i][j] != -1:
                    # Поиск первой подходящей коорднаты
                    ReturnList[0] = i
                    ReturnList[1] = j

    return ReturnList


def Analazing(List):  # Алгоритм анализа ботом текущей ситуации для выбора лучшего решения
    # +++(0) Инициализация
    i = 0
    # бот выставляет только -1, а игрок только +1, поэтому ищем минимальые суммы (минимальные суммы отрицательных элементов). Минимальные суммы запоминаем в MinList
    # MinList устоен следующим образом:
    # 1)первые элементы это минимальое значение сумм в строке и номер строки
    # 2)вторыеые элементы это минимальое значение сумм в столбце и номер столбца
    MinList = [[100, -100], [100, -100], [100, -100]]
    # MinimumInAll - это список с указанием номера строки/столбца/диагонали где наименьшее значение и обозначение, куда ставить следующи выбор:строка/столбец/диагональ
    # строка =0 столбец=1 диагональ=2
    MinimumInAll = [100, -100]
    # ---(0) Инициализация
    # +++(1) Проверка достижений в строках
    SummList = [0, 0, 0]
    for item in List:
        for x in item:
            if x == 1:  # бот выставляет только -1, а игрок только +1
                # Если игрок поставил что от в строке - это строка не рабочая, выходим
                SummList[i] = 3
                break
            elif x == -1:
                SummList[i] += x
        i += 1
    for i in range(len(SummList)):
        if SummList[i] < MinList[0][0]:
            MinList[0][0] = SummList[i]
            MinList[0][1] = i
    # ---(1) Проверка достижений в строках
    # +++(2) Проверка достижений в столбцах
    SummList = [0, 0, 0]
    for j in range(0, 3):
        for i in range(0, 3):
            if List[i][j] == 1:  # бот выставляет только -1, а игрок только +1
                # Если игрок поставил что от в строке - это строка не рабочая, выходим
                SummList[i] = 3
                break
            elif List[i][j] == -1:
                SummList[i] += List[i][j]

    for i in range(len(SummList)):
        if SummList[i] < MinList[1][0]:
            MinList[1][0] = SummList[i]
            MinList[1][1] = i
    # ---(2) Проверка достижений в столбцах
    # +++(3) Проверка достижений в диагонали
    SummList = [0, 0, 0]
    # Первая диагональ
    for j in range(0, 3):
        if List[j][j] == 1:  # бот выставляет только -1, а игрок только +1
            # Если игрок поставил что от в диагонали - это диагональ не рабочая, выходим
            SummList[0] = 3
            break
        elif List[j][j] == -1:
            SummList[0] += List[j][j]

    # Вторая диагональ
    for j in range(2, -1, -1):
        i = abs(j-2)
        if List[i][j] == 1:  # бот выставляет только -1, а игрок только +1
            # Если игрок поставил что-то в диагонали - это диагональ не рабочая, выходим
            SummList[1] = 3
            break
        elif List[i][j] == -1:
            SummList[1] += List[i][j]

    for i in range(len(SummList)-1):
        if SummList[i] < MinList[2][0]:
            MinList[2][0] = SummList[i]
            MinList[2][1] = i  # Номер диагонали
    # ---(3) Проверка достижений в диагонали
    # +++(4) Проверка достижений по всем направлениям
    for i in range(len(MinList)):
        if MinList[i][0] < MinimumInAll[0]:
            MinimumInAll[0] = MinList[i][1]  # Номер строки/столбца/диагонали
            MinimumInAll[1] = i  # строка =0 столбец=1 диагональ=2
    # ---(4) Проверка достижений по всем направлениям

    return MinimumInAll

    # ==========================================================================================================
    # ==========================================================================================================


# task 1
os.system('cls')
print("\n")
print("Задача 1")
print('Создайте программу для игры в ""Крестики-нолики"".\n')

print("===================================")
print("===== ИГРА  НАЧИНАЕТСЯ!!!  ========")
print("===================================\n")


# ++++++(0)Инициализация
# Сисок списков для отображения
DeskList = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
# Сисок списков для подсчета
WinList = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
print("Вы - 1-й игрок\n")
PlayerSelect = randint(1, 2)  # Случайная жеребьевка игрока
print(f"{PlayerSelect} -й игрок начинает ход\n")

inputClick = 0  # количество вводов сделанных игроком
Coordinates = []
answer = ''
# ----(0)Инициализация

# Режим игры с ботом

while CheckIn(WinList) == '' and inputClick < 10:
    if PlayerSelect == 1:  # Играем игроком
        while True:
            InputWord = input(
                f'{PlayerSelect}-й игрок, введите координаты (через пробел 2 числа: натуральные числа от 1 до 3:     ')
            Coordinates = InputWord.split()
            answer = CheckCoordinates(Coordinates)
            if answer == '':
                for i in range(len(Coordinates)):
                    Coordinates[i] = int(Coordinates[i])-1
                WinList[Coordinates[0]][Coordinates[1]] = 1
                DeskList[Coordinates[0]][Coordinates[1]] = 'X'
                inputClick += 1
                break
            else:
                print(answer)
    elif PlayerSelect == 2:  # Играем с ботом
        # Умное поведение бота++++++
        Coordinates = WhereToInput(Analazing(WinList), WinList)
        WinList[Coordinates[0]][Coordinates[1]] = -1
        DeskList[Coordinates[0]][Coordinates[1]] = 'O'
        inputClick += 1
        print(
            f'2-й игрок, ввел координаты:     {Coordinates[0]+1} {Coordinates[1]+1}')

    # Меняем игрока (инициализация перед первой вынужденой заменой - в цикле)
    if PlayerSelect == 1:
        PlayerSelect += 1
    else:
        PlayerSelect -= 1

    show_desc(DeskList)

if PlayerSelect == 1:
    PlayerSelect += 1
else:
    PlayerSelect -= 1

print("===== Результат ========")
# Сообщение о Выйгрыше
print(f'{PlayerSelect}-й игрок выйграл. {CheckIn(WinList)}')
print("=============================\n")
# input("НАЖМИТЕ ANYKEY ДЛЯ ПЕРЕХОДА К СЛЕДУЮЩЕЙ ЗАДАЧЕ   ")

# ==========================================================================================================
# ==========================================================================================================
