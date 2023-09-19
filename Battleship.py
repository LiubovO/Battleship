import random

class Dot:
    miss_shot = "T"
    hit_shot = "X"
    empty_dot = "0"
    ship_dot = "■"
    ship_cont = "T"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)
        
class Ship:
    def __init__(self, length, x, y, direction=0):
        self.length = length
        self.x = x
        self.y = y
        self.direction = direction
        self.lives = length
        self.ship_dots= []
        self.ship_contur=[]
    
    def dots(self):
        self.ship_dots = []
        if self.direction == 0:
            for dot in range(self.length):
                self.ship_dots=self.ship_dots + [Dot(self.x-1, self.y + dot-1)]
        else:
            for dot in range(self.length):
                self.ship_dots=self.ship_dots + [Dot(self.x+ dot-1, self.y-1)]
        return self.ship_dots   
        
    def contour(self,ship_dots):
        for dot in self.ship_dots:
            for i in range(dot.x - 1, dot.x + 2):
                for j in range(dot.y - 1, dot.y + 2):
                    if Dot(i, j) not in self.ship_contur and Dot(i, j) not in self.ship_dots and 0 <= i < 6 and 0 <= j < 6:
                        self.ship_contur = self.ship_contur + [Dot(i, j)]
            return self.ship_contur    
    
        
        
class Board:  
    def __init__(self, board=None, ships=None, hid=False, active_ships=0):
        if ships is None:
            ships = []
        if board is None:
            board = [[Dot.empty_dot] * 6 for _ in range(6)]
        self.board = board
        self.ships = ships
        self.hid = hid
        self.active_ships = active_ships
        self.ship_contour = []
        self.shot_dots = []
        self.ship_list = []

    def print_board(self):  
        if not self.hid:
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
                
    def add_ship(self, ship_dots, ship_contur, hid, ship):
        try:
            for dot in ship_dots:
                if dot in self.ships or dot in self.ship_contour or dot.x > 5 or dot.y < 0 or dot.y > 5:
                    raise IndexError
            
            self.ships=self.ships+ship_dots
            self.ship_list = self.ship_list + [ship]
            if hid is False:
                for dot in ship_dots:
                    self.board[dot.x][dot.y]=dot.ship_dot
            for dot in ship_contur:
                self.ship_contour=self.ship_contour+[dot]
            self.active_ships = self.active_ships + 1    
            return self.board, self.ships, self.ship_contour, self.active_ships
        
        except IndexError:
            if hid is False:  
                print("Клетка занята, либо ввод некорректный. Пожалуйста, попробуйте ещё раз")   

                
    def shot(self, shot_dot, hid=False):
        try:
            if shot_dot in self.shot_dots or \
                    shot_dot.x < 0 or shot_dot.x > 6 or shot_dot.y < 0 or shot_dot.y > 6:  
                raise IndexError    
            self.shot_dots = self.shot_dots + [shot_dot]
            if shot_dot in self.ships:  
                self.board[shot_dot.x][shot_dot.y] = shot_dot.hit_shot
                ship_counter=-1
                for dot in self.ship_list:
                    ship_counter=ship_counter+1
                    for j in dot.ship_dots:
                        if shot_dot==j:
                            self.ship_list[ship_counter].lives = self.ship_list[ship_counter].lives -1 
                            if dot.lives==0:
                                self.active_ships = self.active_ships - 1 
                                for c in dot.ship_contur:
                                    self.board[c.x][c.y]=c.ship_cont
                                if hid is False:
                                    print("Корабль потоплен!")
                                    break
                            elif hid is False:
                                print("Корабль поврежден!")
                                break
            else:
                print("Мимо!")
                self.board[shot_dot.x][shot_dot.y]=shot_dot.miss_shot
                
            return self.board
        except IndexError:
            if hid is False:
                print("Попробуйте другие координаты выстрела.Возможно Вы сюда уже стреляли.")
                
class Player:
    def __init__(self, player, my_board, other_board, shot_dot=None, hid=True):
        self.player=player
        self.my_board=my_board
        self.other_board=other_board
        self.shot_dot = shot_dot
        self.hid = hid
        
    def ask(self):
        return self.shot_dot
        
    def move(self, hid=False):
        self.other_board.shot(self.shot_dot, self.hid)
        if hid is False:
            print("Ваше игровое поле", "\n")
        else:
            print("Игровое поле компьютера", "\n")
        self.other_board.print_board()  
        if self.other_board.active_ships == 0:
            print("Побеждает", self.player, "\n")
            
class User(Player):
    def __init__(self, my_board, other_board, player= "Пользователь", hid=False):
        super().__init__(player, my_board, other_board, shot_dot=None, hid=True)
        self.player = player
        self.hid = hid
        
    def ask(self):
        print("Введите координаты выстрела: X - столбец, Y- строка")
        x=int(input("X:"))-1
        y=int(input("Y:"))-1
        self.shot_dot = Dot(x, y)
        return self.shot_dot
        
class Computer(Player):
    def __init__(self, my_board, other_board, player= "Компьютер", hid=True):
        super().__init__(player, my_board, other_board, shot_dot=None, hid=True)
        self.player = player
        self.hid = hid
        
    def ask(self):
        self.shot_dot = Dot(random.randint(0, 5), random.randint(0, 5))
        return self.shot_dot

class Game:
    def __init__(self, player=None, computer=None):
        self.player=player
        self.player_board= Board()
        self.computer= computer
        self.computer_board= Board()
        self.ships_sizes= (3,2,2,1,1,1,1)
        self.ship_names= ("трехпалубный", "двухпалубный", "двухпалубный", "однопалубный", "однопалубный", "однопалубный", "однопалубный")
        
    def gen_player_board(self):
        print(self.player_board.print_board())
        ship_count = 0  
        ship_name_count = -1  
        for ship_size in self.ships_sizes:
            ship_count = ship_count + 1  
            ship_name_count = ship_name_count + 1  
            while True:
                print("Устанавливаем ", self.ship_names[ship_name_count])
                if ship_size > 1:
                    ship = Ship(ship_size, int(input("Введите координату X:")), int(input("Введите координату Y:")),
                                int(input('Введите направление')))
                else:  
                    ship = Ship(ship_size, int(input("Введите координату X:")), int(input("Введите координату Y:")))
                self.player_board.add_ship(ship.dots(), ship.contour(ship.dots()), False, ship)
                if self.player_board.active_ships == ship_count:
                    self.player_board.print_board()
                    break
        return self.player_board
        
    def gen_computer_board(self): 
        attempt_count = 0  
        while self.computer_board.active_ships != 7:
            ship_count = 0  
            for ship_size in self.ships_sizes:
                ship_count = ship_count + 1  
                if attempt_count > 100:  
                    attempt_count = 0  
                    break
                while True:
                    ship = Ship(ship_size, random.randint(1, 6), random.randint(1, 6), random.randint(0, 1))
                    self.computer_board.add_ship(ship.dots(), ship.contour(ship.dots()), True, ship)
                    attempt_count = attempt_count + 1  
                    if attempt_count > 100:  
                        self.computer_board = Board() 
                        break
                    if self.computer_board.active_ships == ship_count:
                        attempt_count = 0 
                        break
        return self.computer_board
        
    def game_loop(self): 
        pl = User(my_board=g.player_board, other_board=g.computer_board)
        ai = Computer(my_board=g.computer_board, other_board=g.player_board)
        while True:
            pl.ask()
            pl.move(hid=True)
            ai.ask()
            ai.move(hid=False)
            if pl.other_board.active_ships == 0 or ai.other_board.active_ships == 0:
                break

    def greeting(self):
        print("Добро пожаловать в Морской бой!:"
              "\n1. Против Вас играет компьютер"
              "\n2. Перед Вами поле 6х6 клеток"
              "\n3. Для начала расставим корабли"
              "\n4. Наш флот: 1 трехпалубный, 2 двухпалубных и 4 однопалубных корябля"
              "\n5. Вводим координаты носа корабля (X - столбец, Y - строка)"
              "\nи направление расположения для длинных кораблей"
              "\n 0 - горизонтальное, 1 - вертикальное"
              "\n4. Ставить корабли в соседних точках друг с другом нельзя, в этом случае будет предложена"
              "\nповторная попытка"
              "\n5. Компьютер расставляет свои корабли автоматически"
              "\n6. Далее игроки (Вы и компьютер) по очереди делаете выстрелы, вводя координаты X и Y"
              "\n7. Стрелять вне доски либо в точку, куда ранее стреляли - нельзя, в этом случае будет предложен"
              "\nповторный ход"
              "\n8. После выстрела будет выведено сообщение о результате - промах, либо корабль подбит, либо уничтожен"
              "\n9. Подбитые корабли обозначаются крестиком, промахи - буквой Т"
              "\n10. Если Вы уничтожили корабль противника, на игровой доске противника он будет для удобства"
              "\nобведен контуром - туда стрелять смысла нет"
              "\n11. После каждого хода будет выводится Ваша доска с результатами стрельбы противника, и доска"
              "\nпротивника с результатами Вашей стрельбы"
              "\n12. Выигрывает тот, кто первый уничтожит все корабли противника"
              "\n УДАЧИ!"
              "\n")


g = Game()
g.greeting()
g.gen_player_board()
g.gen_computer_board()
g.game_loop()    

