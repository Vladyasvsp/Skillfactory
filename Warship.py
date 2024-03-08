from random import randint
class Dot: #класс точки
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other): #метод для сравнение точек
        return self.x == other.x and self.y == other.y

    def __repr__(self): #метод для вывода точек
        return f"Dot({self.x}, {self.y})"

class BoardException(Exception): #Исключения
    pass

class BoardOutException(BoardException): #За доску
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску"

class BoardUsedException(BoardException): #Повторный выстрел в ту же клетку
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException): #Для размещения кораблей
    pass

class Ship: #класс корабли
    def __init__ (self, bow, l, o):
        self.bow = bow #корабль
        self.l = l      #длина
        self.o = o      #ориентация
        self.lives = l  #жизни

    @property
    def dots(self): #метод расстановки корабля
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x #нос корабля
            cur_y = self.bow.y

            if self.o == 0: #ориентирование
                cur_x += i #по горизонтали

            elif self.o == 1:
                cur_y += i  #по вертикали

            ship_dots.append(Dot(cur_x, cur_y)) #список точек корабля

        return ship_dots

    def shooten(self, shot): #метод для определения попадания
        return shot in self.dots

class Board:    #класс поле
    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid

        self.count = 0 #кол-во пораженных кораблей

        self.field = [ ["O"]*size for _ in range(size) ] #атрибут, показывающий пустую клетку

        self.busy = []  #занятые точки
        self.ships = [] #список кораблей

    def __str__(self): #вывод доски
        res = ""
        res += "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n {i+1} | " + " | ".join(row) + " |"

        if self.hid: #для скрытия доски
            res = res.replace("■", "O")
        return res

    def out(self, d): #метод проверки точки на доске
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb = False): #метод контура корабля
        near = [                    #список точек вокруг корабля
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship): #метод для добавления корабля
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d): #метод  выстрела
        if self.out(d): #точка за пределами
            raise BoardOutException()

        if d in self.busy: #точка занята
            raise BoardUsedException()

        self.busy.append(d) #занимаем точку

        for ship in self.ships: #выстрел
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0: #уничтожен
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return False
                else: #ранен
                    print("Корабль ранен")
                    return True

        self.field[d.x][d.y] = "." #выстрел мимо
        print("Мимо!")
        return False

    def begin(self): #обнуление списка при начале игры
        self.busy = []

class Player: #класс игрок
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player): #класс игрок-компьютер
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y +1}")
        return d

class User(Player): #класс игрок-пользователь
    def ask(self):
       while True:
           cords = input("Ваш ход: ").split()

           if len(cords) != 2:
               print("Введите 2 координаты!")
               continue

           x, y = cords

           if not (x.isdigit()) or not (y.isdigit()):
               print("Введите число!")
               continue

           x, y = int(x), int(y)

           return Dot(x - 1, y - 1)

class Game: #класс игры
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board
           
    def try_board(self): #метод создания доски
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board
    def greet(self):
        print("   Приветствуем Вас в игре   ")
        print("          Морской бой        ")
        print("")
        print("Формат ввода: x y")
        print("x - номер строки")
        print("y - номер столбца")


    def loop(self):
        num = 0
        while True:
            print("Доска пользователя:")
            print(self.us.board)
            print("-"*10)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("Ходит пользователь")
                repeat = self.us.move()
            else:
                print("Ходит компьютер")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("Пользователь выиглал")
                break

            if self.us.board.count == 7:
                print("Компьютер выиграл")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()




        
        



