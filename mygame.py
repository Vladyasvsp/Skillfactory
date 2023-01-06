def hello(): #Приветсвие
    print('  Игра "Крестики-нолики"')
    print('формат ввода: x y')
    print('x - номер строки от 0 до 2')
    print('y - номер столбца от 0 до 2')

def table(): #Поле
    print(f'  0 1 2')
    for i in range(3):
        row_info = ' '.join(game[i])
        print(f'{i} {row_info}')

def hod(): #Проверка хода
    while True:
        cords = input('Ваш ход:').split()

        if len(cords) != 2:
            print('Введите 2 координаты')
            continue
        x, y = cords

        if not (x.isdigit()) or not (y.isdigit()):
            print('Введите числа')
            continue
        x, y = int(x), int(y)

        if 0 > x or x > 2 or 0 > y or y > 2:
            print('Координаты вне диапазона')
            continue

        if game[x][y] != ' ':
            print('Клетка занята')
            continue

        return x, y

def win(): #Проверка победителя
    win_cord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for cord in win_cord:
        symbols = []
        for c in cord:
            symbols.append(game[c[0]][c[1]])
        if symbols == ['X', 'X', 'X']:
            print('Выиграл Х!')
            return True
        if symbols == ['0', '0', '0']:
            print('Выиграл 0!')
            return True
    return False

hello()
game = [[' ']*3 for i in range(3)]
num = 0 #Счетчик ходов

while True: #Запись в поле
    num +=1
    table()

    if num % 2 == 1:
        print('Ходит крестик')
    else:
        print('Ходит нолик')

    x, y = hod()

    if num % 2 == 1:
        game[x][y] = 'X'
    else:
        game[x][y] = '0'

    if win():
        break

    if num == 9:
        print('Ничья')
        break
