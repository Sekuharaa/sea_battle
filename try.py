import random


class Dot:
    miss_shot = "T"
    hit_shot = "X"
    free_dot = "0"
    ship_dot = "■"
    ship_cont = "*"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

class Board:
    def __init__(self, visible=False):
        self.board = [[Dot.free_dot] * 6 for _ in range(6)]
        self.ships = []
        self.occup_dot = []
        self.shots = []
        self.visible = visible
        self.ships_hp = 0

    def print_board(self):  # print playing field
        for i in range(7):
            if i == 0:
                i = " "
            print(i, end=" ")
        print()
        for i in range(6):
            for j in range(6):
                if j == 0:
                    print(i + 1, self.board[i][j], end=" ")
                else:
                    print(self.board[i][j], end=" ")
            print()
        return self.board

    def add_ship(self, ship, visible=True):
        try:
            for dot in ship.ship_main():
                if dot in self.occup_dot or dot.x < 0 or dot.x > 5 or dot.y < 0 or dot.y > 5:
                    raise IndexError
            for dot in ship.ship_main():
                if visible == True:
                    self.board[dot.x][dot.y] = dot.ship_dot
                else:
                    self.board[dot.x][dot.y] = dot.free_dot
            self.ships.append(ship)
            self.ships_hp += ship.size
            self.occup_dot = self.occup_dot + ship.ship_main()
            self.occup_dot = self.occup_dot + ship.ship_cont(ship.ship_main())
            return self.board, self.ships, self.occup_dot
        except IndexError:
            if visible is True:
                print("Ошибка расположения")
            return False
        return self.ships_hp

    def shot(self, cord, visible=True):
        try:
            shot = Dot((cord.x - 1), (cord.y - 1))
            if shot.x < 0 or (cord.x - 1) > 5 or (cord.y - 1) < 0 or (cord.y - 1) > 5 or Dot((cord.x - 1), (cord.y - 1)) in self.shots or \
                    self.board[(cord.x - 1)][(cord.y - 1)] == Dot.ship_cont:
                raise IndexError
            try:
                for ship in self.ships:
                    for dot in ship.ship_main():
                        if shot in ship.ship_main():
                            self.board[(cord.x - 1)][(cord.y - 1)] = Dot.hit_shot
                            self.ships_hp -= 1
                            ship.ship_hp -= 1
                            if ship.ship_hp == 0:
                                for dot in ship.ship_contur:
                                    self.board[dot.x][dot.y] = Dot.ship_cont
                                    self.shots = self.shots + [Dot((cord.x - 1), (cord.y - 1))]
                            raise StopIteration
                        else:
                            self.board[(cord.x - 1)][(cord.y - 1)] = Dot.miss_shot
                            self.shots = self.shots + [Dot((cord.x - 1), (cord.y - 1))]
            except StopIteration:
                pass
        except IndexError:
            if visible is True:
                print("Ошибка выстрела")
                raise IndexError
        return self.shots

class Ship:
    def __init__(self, x, y, size, comp, ship_dot=None):
        self.x = x
        self.y = y
        self.size = size
        self.ship_hp = size
        self.comp = comp
        self.ship_dot = ship_dot
        if ship_dot is None:
            ship_dot = []
        self.ship_contour = []

    def ship_main(self):
        self.ship_dot = []
        if self.comp == 1:
            for dot in range(self.size):
                self.ship_dot.append(Dot(self.x - 1 + dot, self.y - 1))
        else:
            for dot in range(self.size):
                self.ship_dot.append(Dot(self.x - 1, self.y - 1 + dot))
        return self.ship_dot

    def ship_cont(self,ship_dot):
        for dot in self.ship_dot:
            for i in range(dot.x - 1, dot.x + 2):
                for j in range(dot.y - 1, dot.y + 2):
                    if Dot(i, j) not in self.ship_contour and Dot(i,j) not in self.ship_dot and 0 <= i <= 5 and 0 <= j <= 5:
                        self.ship_contur = self.ship_contour + [Dot(i, j)]
        return self.ship_contour

class Player:
    def __init__(self,my_board, your_board):
        self.my_board = my_board
        self.your_board = your_board

    def ask_shot (self):
        cord = Dot
        try:
            x = int(input("Cтрока"))
            y = int(input("Cтолбец"))
        except TypeError:
            print("Ошибка ввода")
        return cord(x, y)

class AI:
    def __init__(self, my_board, your_board):
        self.my_board = my_board
        self.your_board = your_board

    def ask_shot(self):
        cord = Dot
        x = random.randint(1,6)
        y = random.randint(1,6)
        return cord(x, y)

class Game:
    def __init__(self, shot=None):
        self.ship_size_list = [3, 2, 2, 1, 1, 1, 1]
        self.shot = shot

    def gen_user_board(self):
        board_user = Board()
        board_user.print_board()
        ship_count = 0
        while ship_count != 7:
            x = int(input("Размещение кораблей.Строка: "))
            y = int(input("Столбец: "))
            size = self.ship_size_list[ship_count]
            if size == 1:
                comp = 1
            else:
                comp = int(input("Положение: 1-вертикальное,2-горизонтальное "))
            ship = Ship(x,y,size,comp)
            if bool(board_user.add_ship(ship)) == True:
                ship_count += 1
                board_user.print_board()
        else:
            return board_user

    def gen_ai_board(self):
        board_ai = Board()
        ship_count = 0
        ship_count2 = 0
        while ship_count2 != 7:
            x = random.randint(1,6)
            y = random.randint(1,6)
            size = self.ship_size_list[ship_count2]
            if size == 1:
                comp = 1
            else:
                comp = random.randint(1,2)
            ship = Ship(x,y,size,comp)
            if bool(board_ai.add_ship(ship, visible=False)) == True:
                ship_count2 += 1
            else:
                ship_count += 1
                if ship_count > 100:
                    ship_count = 0
                    ship_count2 = 0
                    board_ai = Board()
                    return g.gen_ai_board()
        else:
            return board_ai

    def start(self,board_user,board_ai):
        self.board_user = board_user
        self.board_ai = board_ai
        self.board_user.print_board()
        self.board_ai.print_board()
        print("Начинаем игру!!!")

    def gaming (self):
        ai = AI(self.board_ai, self.board_user)
        pl = Player(self.board_user,self.board_ai)
        while True:
            while True:
                try:
                    self.board_ai.shot(pl.ask_shot())
                    break
                except IndexError:
                    print("Неверные координаты")
                    self.board_ai.print_board()
                except ValueError:
                    print("Неверный выстрел")
                    self.board_ai.print_board()
            print("Поле ИИ")
            self.board_ai.print_board()
            while True:
                try:
                    self.board_user.shot(ai.ask_shot(), visible=False)
                    break
                except IndexError:
                    None
                except ValueError:
                    None
            print("Поле игрока")
            self.board_user.print_board()
            if self.board_ai.ships_hp == 0:
                print("Игрок победил!")
                break
            if self.board_user.ships_hp == 0:
                print("Компьютер победил!")
                break

g = Game()

g.start(g.gen_ai_board(),g.gen_user_board())
g.gaming()