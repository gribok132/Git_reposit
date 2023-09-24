import random


class Dot:
    type = "dot"
    empty_dot = "O |"
    ship_dot = "# |"
    destroyed_ship_dot = "X |"
    missed_dot = "T |"
    hidden_ship_dot = "O |"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        return False


class Ship:
    def __init__(self, length, direction, bow_of_ship):
        self.length = length
        self.hp = length
        self.direction = direction
        self.bow_of_ship = bow_of_ship  # Нос корабля

    def dots(self):
        ship_dotes = []
        if self.direction == 0:  # - Вертикальное направление корaбля, нос корабля сверху
            for i in range(self.length):
                ship_dotes.append(Dot(self.bow_of_ship[0], self.bow_of_ship[1] + i))
        else:  # - горизонтальное направление корaбля, нос корабля слева
            for i in range(self.length):
                ship_dotes.append(Dot(self.bow_of_ship[0] + i, self.bow_of_ship[1]))
        return ship_dotes

    def contour(self):  # У каждого корабля имеется свой контур
        contour_dotes = []
        for dot in self.dots():
            for i in range(-1, 2):
                for j in range(-1, 2):
                    contour_dotes.append(Dot(dot.x + i, dot.y + j))
        return contour_dotes


class Board:
    def __init__(self, size=6, hid=True):
        self.board = [["  |", "1 |", "2 |", "3 |", "4 |", "5 |", "6 |", " "],
                      ["1 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      ["2 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      ["3 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      ["4 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      ["5 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      ["6 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "]]
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == " O |" or self.board[x][y] == " O":
                    self.board[x][y] = Dot.empty_dot

        self.size = size
        self.hid = hid
        self.ships = []
        self.alive_ships = 0

    def clear(self):  # Метод очистки поля
        self.board = [["  |", "1 |", "2 |", "3 |", "4 |", "5 |", "6 |", " "],
                      ["1 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      ["2 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      ["3 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      ["4 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      ["5 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      ["6 |", " O |", " O |", " O |", " O |", " O |", " O", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "]]
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == " O |" or self.board[x][y] == " O":
                    self.board[x][y] = Dot.empty_dot
        self.alive_ships = 0
        self.ships = []

    def hide_board(self):  # Метод маскировки кораблей
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == Dot.ship_dot:
                    self.board[x][y] = Dot.hidden_ship_dot

    def is_hidden(self):  # Отличие поля врага от поля игрока
        return self.hid

    def generate_board(self):  # Метод отображения поля
        for cell in self.board:
            print(*cell)

    def add_ship(self, ship):
        try:
            for dot in ship.dots():
                for c_dot in ship.contour():
                    if self.board[dot.x][dot.y] != Dot.empty_dot or self.out(dot) or self.board[c_dot.x][c_dot.y] == Dot.ship_dot:  # Проверка на свободность клетки
                        if self.is_hidden():
                            print("\nНельзя ставить поверх кораблей и их контура!\n\n===========================")
                            return False
                        else:
                            return False
            for dot in ship.dots():  # Ставим корабль
                self.board[dot.x][dot.y] = Dot.ship_dot
            self.ships.append(ship)  # Добавляем корабль в [корабли]
            self.alive_ships += 1
            if self.is_hidden():  # После установки при hid=True выводим карту с новым кораблем
                print("\nКорабль установлен!\n")
                self.generate_board()
                print(f"\nУстановлено кораблей - {self.alive_ships}\n")
                print("=" * 28)
                return True
        except IndexError:
            if self.is_hidden():
                print("Одна или несколько точек находятся не на карте!\n===========================\n")
                return False
            return False

    def out(self, dot):
        return not (1 <= dot.x < self.size + 1 and 1 <= dot.y < self.size + 1)

    def shot(self, dot):
        is_shot = False
        if self.board[dot.x][dot.y] == Dot.empty_dot:
            self.board[dot.x][dot.y] = Dot.missed_dot
        elif self.board[dot.x][dot.y] == Dot.ship_dot or self.board[dot.x][dot.y] == Dot.hidden_ship_dot:
            self.board[dot.x][dot.y] = Dot.destroyed_ship_dot
            is_shot = True
            for ship in self.ships:
                if dot in ship.dots():
                    ship.hp -= 1
                    if ship.hp == 0:  # При уничтожении корабля
                        self.alive_ships -= 1
                        for c_dot in ship.contour():  # Обводим контур полностью подбитого корабля подбитыми клетками
                            if self.board[c_dot.x][c_dot.y] == Dot.missed_dot:
                                continue
                            if self.board[c_dot.x][
                                c_dot.y] == Dot.empty_dot:  # Проверка чтобы не обводить контуром за картой
                                self.board[c_dot.x][c_dot.y] = Dot.destroyed_ship_dot
                        if self.is_hidden():  # Интерфейс
                            print("\n===========================\n\nВаш корабль уничтожен!\n")
                            print("\n         ВАШЕ ПОЛЕ")
                            self.generate_board()
                            print(f"Кораблей на доске - {self.alive_ships}")
                        else:
                            print("\n===========================\n\nВражеский корабль уничтожен!\n")
                            print("\n        ПОЛЕ ВРАГА")
                            self.generate_board()
                            print(f"Кораблей на доске - {self.alive_ships}")
                    else:  # При попадании в корабль
                        if self.is_hidden():
                            print("\n===========================\n\nВраг попал в ваш корабль!\n")
                            print("\n         ВАШЕ ПОЛЕ")
                            self.generate_board()
                            print(f"Кораблей на доске - {self.alive_ships}")
                        else:
                            print("\n===========================\n\nВы попали во вражеский корабль!\n")
                            print("\n        ПОЛЕ ВРАГА")
                            self.generate_board()
                            print(f"Кораблей на доске - {self.alive_ships}")
        return is_shot


class Player:
    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self, board):  # Метод одного хода
        while True:
            try:
                if board.alive_ships == 0:  # Завершение игры
                    print("\n\nИгра окончена!")
                    exit()
                shot_coord = self.ask()
                if board.out(shot_coord):
                    if not board.is_hidden():
                        print("\nТуда стрелять нельзя")
                elif board.board[shot_coord.x][shot_coord.y] == Dot.destroyed_ship_dot:
                    if not board.is_hidden():
                        print("\nВ этой клетке не может быть корабля")
                elif board.board[shot_coord.x][shot_coord.y] == Dot.missed_dot:
                    if not board.is_hidden():
                        print("\nВы уже стреляли в эту клетку")
                result = board.shot(shot_coord)
                if board.is_hidden():  # Если враг попал в корабль, стреляет в соседние клетки
                    while result:
                        random_direction = random.randrange(1, 5)  # Случайное направление для выстрела
                        i = 1
                        if random_direction == 1:
                            result = board.shot(Dot(shot_coord.x + i, shot_coord.y))
                            while result:  # При попадании стреляет в том же направлении пока не промажет
                                i += 1
                                result = board.shot(Dot(shot_coord.x + i, shot_coord.y))
                        elif random_direction == 2:
                            result = board.shot(Dot(shot_coord.x - i, shot_coord.y))
                            while result:
                                i += 1
                                result = board.shot(Dot(shot_coord.x - i, shot_coord.y))
                        elif random_direction == 3:
                            result = board.shot(Dot(shot_coord.x, shot_coord.y + i))
                            while result:
                                i += 1
                                result = board.shot(Dot(shot_coord.x, shot_coord.y + i))
                        elif random_direction == 4:
                            result = board.shot(Dot(shot_coord.x, shot_coord.y - i))
                            while result:
                                i += 1
                                result = board.shot(Dot(shot_coord.x, shot_coord.y - i))
                if board.board[shot_coord.x][shot_coord.y] == Dot.missed_dot:
                    if board.is_hidden():
                        print("\nВраг промазал!\n")
                        print("\n         ВАШЕ ПОЛЕ")
                        board.generate_board()  # Поле игрока после хода врага
                        print("===========================\n")
                        break
                    else:
                        print("\nВы промазали!\n")
                        print("\n        ПОЛЕ ВРАГА")
                        board.generate_board()  # Поле врага после хода игрока
                        print("===========================\n")
                        break
            except IndexError:
                pass


class AI(Player):
    @staticmethod
    def ask(**kwargs):  # Функция случайного выстрела
        x, y = random.randrange(1, 7), random.randrange(1, 7)
        return Dot(x, y)


class User(Player):
    @staticmethod
    def ask(**kwargs):  # Функция спрашивает и передает данные выстрела
        print("Выстрел")
        dot_x, dot_y = "", ""
        while not dot_x.isdigit() or not dot_y.isdigit():
            dot_x, dot_y = input("x:"), input("y:")
            if not dot_x.isdigit() or not dot_y.isdigit():
                print("\nВведите целое число\n")
            continue
        # Данный алгоритм с необходим, чтобы обработать все исключения, включая ввод букв. Реализован со всеми input()

        return Dot(int(dot_y), int(dot_x))

    @staticmethod
    def ask_ship(length):  # Функция спрашивает и передает данные корабля
        x_coord, y_coord = "", ""
        while not x_coord.isdigit() or not y_coord.isdigit():
            x_coord = input("\n[+]Ведите координату х корабля: ")  # #Обработать исключения
            y_coord = input("[+]Ведите координату y корабля: ")  # #Обработать исключения
            if not x_coord.isdigit() or not y_coord.isdigit():
                print("\nВведите число\n")
            continue
        bow_of_ship = (int(x_coord), int(y_coord))
        direction = ""
        if length == 1:
            direction = "1"
        while not direction.isdigit():
            direction = input("--Если корабль горизонтальный введите - 0\n--Если корабль вертикальный введите - 1\n[+]Ваш ввод:")
            if not direction.isdigit():
                print("\nВведите число\n")
        ship = Ship(length, int(direction), bow_of_ship)
        return ship


class Game:
    def __init__(self):
        self.user_board = Board(6, True)
        self.enemy_board = Board(6, False)
        self.user = User(self.user_board, self.enemy_board)
        self.ai = AI(self.user_board, self.enemy_board)

    @staticmethod
    def random_board(board):  # Функция случайной генерации поля
        x = 0
        while True:
            x += 1
            ship_3len = Ship(3, random.randrange(0, 2), (random.randrange(1, 7), random.randrange(1, 7)))
            board.add_ship(ship_3len)
            if x > 300:
                return False
            if board.alive_ships == 1:
                break
        while True:
            x += 1
            ship_2len = Ship(2, random.randrange(0, 2), (random.randrange(1, 7), random.randrange(1, 7)))
            board.add_ship(ship_2len)
            if x > 300:
                return False
            if board.alive_ships == 3:
                break
        while True:
            x += 1
            ship_1len = Ship(1, random.randrange(0, 2), (random.randrange(1, 7), random.randrange(1, 7)))
            board.add_ship(ship_1len)
            if x > 300:
                return False
            if board.alive_ships == 7:
                print("\nДоска врага создана\n")
                print("===========================\n")
                board.hide_board()
                return True

    def user_board_call(self):  # Метод расстановки кораблей игрока
        print("\nНеобходимо расставить ваши корабли")
        ship_lengths = [3, 2, 2, 1, 1, 1, 1]
        for length in ship_lengths:
            result = False
            fail_try_counter = 0  # Счетчик неудачных попыток поставить корабль на поле
            while not result:  # Пока не поставит, не терять этот корабль
                ship = self.user.ask_ship(length)
                result = self.user_board.add_ship(ship)
                fail_try_counter += 1
                if fail_try_counter > 1:  # Если не получается создать поле, предлагать пересоздать его
                    restart_board = ""
                    while not restart_board.isdigit():
                        restart_board = input("\n--Если хотите перезапустить построение кораблей введите - 1\n--Если хотите продолжить построение кораблей введите - 0\n[+]Ваш ввод:")
                        if not restart_board.isdigit():
                            print("\nВведите число\n")
                        continue
                    if restart_board == "1":
                        self.user_board.clear()
                        return False
                    elif restart_board != "1" and restart_board != "0":
                        print("\nнеобходимо выбрать между 1 и 0\n")
                    else:
                        fail_try_counter = 0
        return True

    @staticmethod
    def greet():  # Функция приветствия с правилами
        board = [["  |", " 1 |", " 2 |", " 3 |", " 4 |", " 5 |", " 6 |"],
                 ["1 |", " O |", " O |", " O |", " O |", " O |", " O |"],
                 ["2 |", " O |", " O |", " O |", " O |", " O |", " O |"],
                 ["3 |", " O |", " O |", " O |", " O |", " O |", " O |"],
                 ["4 |", " O |", " O |", " O |", " O |", " O |", " O |"],
                 ["5 |", " O |", " O |", " O |", " O |", " O |", " O |"],
                 ["6 |", " O |", " O |", " O |", " O |", " O |", " O |"]]

        board_example = [["  |", " 1 |", " 2 |", " 3 |", " 4 |", " 5 |", " 6 |"],
                         ["1 |", " O |", " O |", " O |", " O |", " O |", " O |"],
                         ["2 |", " O |", " O |", " O |", " O |", " O |", " O |"],
                         ["3 |", " O |", " O |", " O |", " O |", " O |", " O |"],
                         ["4 |", " O |", " # |", " O |", " O |", " O |", " O |"],
                         ["5 |", " O |", " # |", " O |", " O |", " O |", " O |"],
                         ["6 |", " O |", " O |", " O |", " O |", " O |", " O |"]]
        print(f"\nДобро в пожаловать морской бой!\n"
              "Пример игрового поля:\n")
        for i in board:
            print(*i)
        print("\nПравила установки кораблей:\n "
              "-- Вам будут доступны: 1 корабль размера - 3 клетки, 2 корабля - 2 клетки и 4 корабля - 1 клетки.\n"
              " -- Для кораблей размером 3 и 2 клетки, предлагается выбрать клетку для установки носа и его направление.\n"
              " -- Для кораблей размером 1 клетка предлагается только выбрать клетку для установки.\n"
              " -- Корабль нельзя ставить в одну и ту же клетку.\n"
              " -- Вокруг установленных кораблей образуется контур в который также нельзя устанавливать корабли.\n"
              " -- В случае неудачной установки корабля дважды - будет предложено пересоздать поле.\n"
              " -- Пример установки корабля на клетку [4, 2]:\n")
        for i in board_example:
            print(*i)

    def loop(self):
        while True:
            self.user.move(self.enemy_board)
            self.ai.move(self.user_board)

    def start(self):

        self.greet()

        user_board_created = False
        while not user_board_created:  # Пока поле игрока не создано получает False, нужно в случае пересоздания поля
            user_board_created = self.user_board_call()

        enemy_board_created = False
        while not enemy_board_created:  # Пока не получится сгенерировать поле
            self.enemy_board.clear()
            enemy_board_created = self.random_board(self.enemy_board)

        self.loop()


game = Game()
game.start()
