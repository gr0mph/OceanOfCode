import sys
import math
import copy
import random
import time
import gc

AGENT_TORPEDO = 0   # 3,2,1,0
#AGENT_SONAR = 1
AGENT_MINE = 2
AGENT_SILENCE = 1

game_board = [ None , None ]
movement_f = { 'N': None,'S': None,'E': None,'W': None }
#select_a = [ 'TORPEDO' , 'MINE' , 'SILENCE' ]
select_a = [ 'TORPEDO' , 'SILENCE' , 'MINE' ]


WIDTH, HEIGHT, MY_ID, OPP_ID = 0 , 0, 0, 0
TREASURE_MAP = []

STARTING_SYMBOLS = 'S'
FINISHING_SYMBOLS = 'F'
OBSTACLE_SYMBOL = 'x'
EMPTY_SYMBOLS = '.'

DIRS = [('N',-1, 0), ('S',1, 0), ('E',0, 1), ('W',0, -1)]
GET_DIRS = { (-1,0) : 'N' , (1,0) : 'S' , (0,1) : 'E' , (0,-1) : 'W' }
OPP_DIRS = { 'N' : 'S' , 'S' : 'N' , 'E' : 'W' , 'W' : 'E' }
OPPONENT_SET = set()

def read_map():
    global WIDTH, HEIGHT, MY_ID, OPP_ID
    WIDTH, HEIGHT, MY_ID = [int(i) for i in input().split()]
    OPP_ID = (MY_ID + 1) % 2
    global TREASURE_MAP
    for i in range(HEIGHT):
        TREASURE_MAP.append(list(input()))

def t_check_map(TREASURE_MAP):
    for i in range(HEIGHT):
        print(TREASURE_MAP[i],file=sys.stderr)

DEEP = 11
DEEP_SILENCE = 14 #26
SEARCH_OPP_TORPEDO = 20
SEARCH_OPP_TRIGGER = 5

class Node:

    def __init__(self,clone):
        self.x, self.y = 0, 0
        self.privileged_dir, self.possible_dir = None, None
        if clone is not None:
            self.x, self.y = clone.x, clone.y
            self.privileged_dir, self.possible_dir = self.privileged_dir, self.possible_dir

    def __str__(self):
        return f'(x:{self.x},y:{self.y} poss {self.possible_dir} priv {self.privileged_dir}'

    def set_up(self,x_col,y_row):
        self.x, self.y = x_col, y_row

    def update_dir(self,solving,DIRS):
        #REDUCE_MAP = copy.deepcopy(TREASURE_MAP)
        REDUCE_MAP = solving.grid
        self.privileged_dir = copy.deepcopy(DIRS)
        self.possible_dir = copy.deepcopy(DIRS)
        legal = solving.legal

        results = [dir for dir in DIRS if is_direction_legal(self,legal,dir)]

        coord = self.y, self.x
        length = len(results)
        if length <= 1 :
            solving.delete.append(coord)
            REDUCE_MAP[self.y][self.x] = 'x'
        elif length == 2 :
            self.possible_dir = copy.deepcopy(results)
            self.privileged_dir = None
            #self.possible_dir = None
            #self.privileged_dir = copy.deepcopy(results)
            #for orientation, y_drow, x_dcol in self.privileged_dir:
            #    coord = self.y + y_drow, self.x + x_dcol
            solving.risk.append(coord)
            solving.legal.update( { coord : self } )
        else :
            self.possible_dir = copy.deepcopy(results)
            self.privileged_dir = None
            solving.legal.update( { coord : self } )

        return REDUCE_MAP

def is_direction_legal(point,legal,dir):
    orientation, y_drow, x_dcol = dir
    coord = point.y + y_drow, point.x + x_dcol
    return True if coord in legal else False


class PathSolving:
    """Solver for a Hamilton Path problem."""

    def __init__(self, clone):
        """Initialize the HamiltonSolver instance from a grid, which must be a
        list of strings, one for each row of the grid.
        """
        self.grid = None
        self.legal = {} #set()
        self.start = None
        self.risk = []
        self.delete = []
        if clone is not None :
            self.grid = clone.grid
            self.legal = clone.legal
            self.start = clone.start
            self.risk = clone.risk

    def set_up(self,TREASURE_MAP):
        self.grid = copy.deepcopy(TREASURE_MAP)
        self.start = None
        self.legal = {} #set()
        self.risk = []
        for r, row in enumerate(self.grid):
            for c, item in enumerate(row):
                if item in EMPTY_SYMBOLS:
                    self.legal.update( { (r,c) : None } )
                    #self.legal.add((r, c))

    def reset(self):
        # TODO: Trop naze cette fonction...
        self.legal = {} #set()
        for r, row in enumerate(self.grid):
            for c, item in enumerate(row):
                if item in EMPTY_SYMBOLS:
                    self.legal.add((r, c))

    def update(self):
        for l1 in self.legal:
            y_row, x_col = l1
            n1 = Node(None)
            n1.set_up(x_col,y_row)
            self.grid = n1.update_dir(self,DIRS)

        for coord in self.delete:
            del self.legal[coord]

        #coord = next(iter(self.risk))
        #self.update_risk(coord)

        #coord = self.risk[4]
        #self.update_risk(coord)

        coord = self.risk[0]
        self.update_risk(coord)

        #for coord in self.risk:
        #    self.update_risk(coord)

        for i1, coord in enumerate(self.risk):
            print("{} {}".format(i1,coord))

    def update_risk(self,k_coord):
        y_row, x_col = k_coord
        if k_coord not in self.legal:
            self.grid[y_row][x_col] = 'x'
            return

        for t_r in self.grid:
            print(t_r)

        MIN_REQUIRE_DEEP = 4
        soluce = 0

        start_time = time.time()
        r , c = self.legal[k_coord].y, self.legal[k_coord].x
        the_first_node = self.legal[k_coord]

        for d1 in the_first_node.possible_dir:
            print("Starting {}".format(d1))
            dir, y_drow, x_dcol = d1
            start = r + y_drow, c + x_dcol

            # Cache attribute lookups in local variables
            legal = copy.deepcopy(self.legal)
            coord = r , c
            del legal[coord]
            n1 = legal[start]
            coord = n1.y , n1.x
            del legal[coord]
            path = [n1]
            path_append = path.append
            path_pop = path.pop
            print("Starting {}".format(n1))

            iter_dir = [n1.possible_dir]
            while path:
                y_row, x_col = path[-1].y , path[-1].x
                for d1 in iter_dir[-1]:
                    #print(d1)
                    #iter_dir.pop()
                    print("\t\tNode {} Dir {}".format(n1,d1),end='\'')
                    orientation, y_drow, x_dcol = d1
                    time.sleep(1)
                    new_coord = y_row + y_drow, x_col + x_dcol
                    if new_coord in legal and len(legal[new_coord].possible_dir) > 0 :
                        y_row, x_col = new_coord
                        n1 = legal[new_coord]
                        path_append(n1)
                        print("\tLen Path {} N1 = {}".format(len(path),path[-1]))
                        iter_dir.append(n1.possible_dir)
                        del legal[new_coord]

                        if len(path) > MIN_REQUIRE_DEEP :
                            soluce += 1
                            print("HAPPY")
                            for n1 in path:
                                print(n1)
                            break
                    else :
                        print("\tnot in legal")
                else:
                    #print("\t\tEnd LOOP n1 {}".format(n1))
                    n1 = path_pop()
                    coord = n1.y , n1.x
                    #print("\t\tPath Pop LOOP n1 {}".format(n1))
                    #if len(n1.possible_dir) == 0 :
                    #    print("Delete {}".format(coord))
                    #    del legal[coord]
                    #else:
                    legal[coord] = n1
                    #iter_dir.append(n1.possible_dir)
                    iter_dir.pop()

                if len(path) > MIN_REQUIRE_DEEP:
                    print("FIND 2")
                    break

            print("SOLUCE")
            for n1 in path:
                print(n1)
            print("END SOLUCE")

        if soluce < 2 :
            print("({},{}) shall be removed".format(self.legal[k_coord].x,self.legal[k_coord].y))
            y_row, x_col = k_coord
            self.grid[y_row][x_col] = 'x'
            del self.legal[k_coord]

        else :
            print("It's OKAY")





    def coord_random(self):
        node = random.choice(list(self.legal))
        return node

    def read_turn(self,path,turn):
        return path[turn]

    def solve(self):
        """Generate solutions as lists of coordinates."""
        start_time = time.time()
        r , c = self.start
        path = [self.start]
        dirs = copy.deepcopy(DIRS)
        random.shuffle(dirs)
        dirs = [iter(dirs)]

        # Cache attribute lookups in local variables
        path_append = path.append
        path_pop = path.pop
        legal = self.legal
        legal_add = legal.add
        legal_remove = legal.remove
        dirs_append = dirs.append
        dirs_pop = dirs.pop

        while path:
            r, c = path[-1]
            for orientation, dr, dc in dirs[-1]:
                new_coord = r + dr, c + dc
                if new_coord in legal:
                    path_append(new_coord)
                    legal_remove(new_coord)
                    dirs_append(iter(DIRS))
                    if len(path) > DEEP :
                        return path
                    if not legal:
                        return path
                    break

                #elif new_coord in self.finish:
                #    path_append(new_coord)
                #    dirs_append(iter(DIRS))
                #    print("HERE3",file=sys.stderr)
                #    return path

            else:
                legal_add(path_pop())
                dirs_pop()


class HamiltonSolver:
    """Solver for a Hamilton Path problem."""

    def __init__(self, clone):
        """Initialize the HamiltonSolver instance from a grid, which must be a
        list of strings, one for each row of the grid.
        """
        self.grid = None
        self.legal = set()
        self.start = None
        if clone is not None :
            self.grid = clone.grid
            self.legal = clone.legal
            self.start = clone.start

        self.finish = None

    def set_up(self,TREASURE_MAP):
        self.grid = TREASURE_MAP
        self.start = None
        self.finish = None
        self.legal = set()
        for r, row in enumerate(self.grid):
            for c, item in enumerate(row):
                if item in STARTING_SYMBOLS:
                    self.start = (r, c)
                elif item in FINISHING_SYMBOLS:
                    self.finish = (r, c)
                elif item in EMPTY_SYMBOLS:
                    self.legal.add((r, c))

    def reset(self):
        self.legal = set()
        for r, row in enumerate(self.grid):
            for c, item in enumerate(row):
                if item in STARTING_SYMBOLS:
                    self.start = (r, c)
                elif item in FINISHING_SYMBOLS:
                    self.finish = (r, c)
                elif item in EMPTY_SYMBOLS:
                    self.legal.add((r, c))

    def coord_random(self):
        new_coord = random.choice(list(self.legal))
        return new_coord

    def read_turn(self,path,turn):
        return path[turn]

    def solve(self):
        """Generate solutions as lists of coordinates."""
        start_time = time.time()
        r , c = self.start
        path = [self.start]
        dirs = copy.deepcopy(DIRS)
        random.shuffle(dirs)
        dirs = [iter(dirs)]

        # Cache attribute lookups in local variables
        path_append = path.append
        path_pop = path.pop
        legal = self.legal
        legal_add = legal.add
        legal_remove = legal.remove
        dirs_append = dirs.append
        dirs_pop = dirs.pop

        while path:
            r, c = path[-1]
            for orientation, dr, dc in dirs[-1]:
                new_coord = r + dr, c + dc
                if new_coord in legal:
                    path_append(new_coord)
                    legal_remove(new_coord)
                    dirs_append(iter(DIRS))
                    if len(path) > DEEP :
                        return path
                    if not legal:
                        return path
                    break

                #elif new_coord in self.finish:
                #    path_append(new_coord)
                #    dirs_append(iter(DIRS))
                #    print("HERE3",file=sys.stderr)
                #    return path

            else:
                legal_add(path_pop())
                dirs_pop()

class MineAndTrigger():

    def __init__(self,clone):
        self.treasure_map = None
        self.minefield = set()
        self.legal = set()
        if clone is not None :
            self.minefield = clone.minefield
            self.legal = clone.legal
            self.treasure_map = clone.treasure_map

    def set_up(self,TREASURE_MAP):
        self.treasure_map = TREASURE_MAP
        for y_row, row in enumerate(self.treasure_map):
            for x_col, item in enumerate(row):
                if item in EMPTY_SYMBOLS:
                    self.legal.add( (y_row, x_col) )

    def mine(self,board):
        dirs = [iter(DIRS)]
        orientation, y_drow, x_dcol = '', 0, 0
        for orientation, y_drow, x_dcol in dirs[-1]:
            new_coord = board.y + y_drow, board.x + x_dcol
            if new_coord in self.legal:
                self.legal.remove(new_coord)
                mine = Point(board.x + x_dcol,board.y + y_drow)
                self.minefield.add(mine)
                break
        else:
            return None

        return orientation

    def trigger(self,mine):
        new_coord = mine.y, mine.x
        self.legal.add(new_coord)
        self.minefield.remove(mine)

    def nearby(self,my_board,opp_board):
        for mine in self.minefield:
            if square(mine,my_board) == True:
                continue
            if square(mine,opp_board) == True:
                return mine
        return None

    def __iter__(self):
        for m1 in self.minefield:
            yield m1


class StalkAndLegal():

    def __init__(self,clone):
        self.legal = set()
        if clone is not None:
            self.legal = copy.deepcopy(clone.legal)

    def __str__(self):
        text = ''
        for y_row, x_col in self.legal:
            text = '{} ({},{})'.format(text,x_col,y_row)
        return text

    def set_up(self,TREASURE_MAP):
        for y_row, row in enumerate(TREASURE_MAP):
            for x_col, item in enumerate(row):
                if item in EMPTY_SYMBOLS:
                    #print('({},{})'.format(y_row,x_col))
                    self.legal.add((y_row, x_col))

    def read_move(self,point,dy_row,dx_col):
        new_coord = point.y + dy_row , point.x + dx_col
        if new_coord in self.legal:
            self.legal.remove(new_coord)
            return True
        return False

    def read_surface(self,submarine):
        self.legal.clear()
        self.set_up(submarine.treasure_map)
        new_coord = submarine.y , submarine.x
        self.legal.remove(new_coord)

    def read_silence(self,board1,length1,dy_row,dx_col):
        legal = self.legal
        legal_remove = self.legal.remove
        for i1 in range(1,length1+1):
            new_coord = board1.y + i1 * dy_row , board1.x + i1 * dx_col
            if new_coord in legal:
                legal_remove(new_coord)
            else :
                return False
        return True


class StalkAndTorpedo():

    def __init__(self,clone):
        self.treasure_map = None
        self.out = set()
        self.inp = set()
        if clone is not None :
            self.treasure_map, self.inp = clone.treasure_map, clone.out

    def __str__(self):
        text = ''
        for board_in, stalk_in in self.inp:
            text = '{}\n({},{},life{})'.format(text,board_in.x, board_in.y, board_in.life)
        return text

    def set_up(self,TREASURE_MAP):
        inp_add = self.inp.add
        new_board, new_stalk = None, None
        self.treasure_map = TREASURE_MAP
        for y_row, row in enumerate(self.treasure_map):
            for x_col, item in enumerate(row):
                if item in EMPTY_SYMBOLS:
                    new_board = Board(None)
                    new_board.x, new_board.y = x_col, y_row

                    new_stalk = StalkAndLegal(None)
                    new_stalk.set_up(self.treasure_map)

                    inp_add((new_board,new_stalk))

    def update(self,action,data):
        action(self,data)

    def read_move(self,data):
        data = data[0]
        d, dy_row, dx_col = next( result_dir for result_dir in DIRS if data in result_dir )
        for board,stalk in self.inp:
            result = stalk.read_move(board,dy_row,dx_col)
            if result == True :
                board.x, board.y = board.x + dx_col, board.y + dy_row
                self.out.add( (board,stalk) )

    def read_surface(self,data):
        for board, stalk in self.inp:
            board.life -= 1
            if board.life > 0 :
                # Reset TREASURE MAP for board, don't know If it's very necessary
                board.treasure_map = copy.deepcopy(TREASURE_MAP)
                stalk.read_surface(board)
                self.out.add( (board,stalk) )

    def read_torpedo(self,data):
        x, y = int(data[0]), int(data[1])
        point = Point(x,y)
        for board, stalk in self.inp:
            distance = manhattan(board,point)
            if distance <= 4 :
                self.out.add( (board,stalk) )

    def read_silence(self,data):
        inp = self.inp
        out_add = self.out.add
        if len(self.inp) >= DEEP_SILENCE:
            self.inp.clear()
            self.set_up(self.treasure_map)
            self.out = self.inp

        else :
            for board, stalk in inp:
                # Length 0
                out_add( (board, stalk))

                for orientation, dy_row, dx_col in DIRS:
                    for length1 in range(1,5):
                        board1, stalk1 = Board(board), StalkAndLegal(stalk)
                        result = stalk1.read_silence(board1,length1,dy_row,dx_col)
                        if result == True :
                            board1.x, board1.y = board1.x + length1 * dx_col, board1.y + length1 * dy_row
                            out_add( (board1,stalk1) )
                        else :
                            break

READ_COMMAND = [
( 'MOVE' , StalkAndTorpedo.read_move ),
( 'SURFACE' , StalkAndTorpedo.read_surface ),
( 'TORPEDO' , StalkAndTorpedo.read_torpedo ),
( 'SONAR' , None ),
( 'SILENCE' , StalkAndTorpedo.read_silence )
]

MINE_MAP = []
#MINE_MAP.append(list('               '))
#MINE_MAP.append(list(' . .  . .  . . '))
#MINE_MAP.append(list('  .    .    .  '))
#MINE_MAP.append(list(' . .  . .  . . '))
#MINE_MAP.append(list('               '))
#MINE_MAP.append(list('               '))
#MINE_MAP.append(list('               '))
#MINE_MAP.append(list('               '))
#MINE_MAP.append(list('               '))
#MINE_MAP.append(list('               '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('  .    .    .  '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('  .    .    .  '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('  .    .    .  '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('               '))


class Point():

    def __init__(self,x,y):
        self.x, self.y = x, y

    def __str__(self):
        return f'({self.x},{self.y})'

class Mine(Point):

    def __init__(self,x,y):
        super().__init__(x,y)
        self.nb = 0

class Submarine():

    def __init__(self,clone):
        self.out = ''
        self.treasure_map = TREASURE_MAP
        if clone is not None :
            self.x, self.y = clone.x, clone.y
        else :
            self.x, self.y = 0, 0


    # MOVE DIRECTION {NORTH, EAST, WEST, SOUTH} LOAD {TORPEDO,SONAR,etc}
    def write_move(self,direction,load):
        t = f'MOVE {direction} {load}'
        self.out = t if self.out == '' else f'{self.out} | {t}'

    def write_silence(self,direction,length):
        t = f'SILENCE {direction} {length}'
        self.out = t if self.out == '' else f'{self.out} | {t}'

    def write_surface(self):
        self.out = 'SURFACE' if self.out == '' else f'{self.out} | SURFACE'

    def write_torpedo(self,x,y):
        t = f'TORPEDO {x} {y}'
        self.out = t if self.out == '' else f'{self.out} | {t}'

    def write_mine(self,direction):
        t = f'MINE {direction}'
        self.out = t if self.out == '' else f'{self.out} | {t}'

    def write_trigger(self,x,y):
        t = f'TRIGGER {x} {y}'
        self.out = t if self.out == '' else f'{self.out} | {t}'

    # TODO -->
    def read_move(self,direction):
        # IF OKAY
        return True if True else None

    # TODO -->
    def read_surface(self,sector):
        # IF submarine in SECTOR
        return True if True else None

    # TODO -->
    def read_torpedo(self,x,y):
        # THE OPPONENT CAN BE STUPID TO LAUNCH A TOPEDO WHERE IT IS
        # CONSIDER THA WILL NOT DO THAT
        # Return OKAY IF X AND Y DIFFER
        return True if True else None

    def order(self):
        print(self.out)

class Board(Submarine):

    def __init__(self,clone):
        super().__init__(clone)
        self.turn = 0
        self.x , self.y , self.life = 0, 0, 6
        self.torpedo, self.sonar, self.silence, self.mine = 0, 0, 0, 0
        if clone is not None:
            self.turn = clone.turn + 1
            self.x, self.y, self.life = clone.x, clone.y, clone.life
            self.torpedo, self.sonar = clone.torpedo, clone.sonar
            self.silence, self.mine = clone.silence, clone.mine



def update(me,opp):
    me.x, me.y, me.life, opp.life, me.torpedo, me.sonar, me.silence, me.mine = [int(i) for i in input().split()]

def update_order(text):
    text, t1 = text.split('|'), ''
    for t1 in text:
        #print(". update order: {}".format(t1), flush = True, file=sys.stderr)
        try:
            c1, f1 = next( (c1,f1) for c1,f1 in READ_COMMAND if t1.find(c1) != -1 )
            t_list = t1.split(' ')
            _,d1 = t_list[0], t_list[1:]
            yield c1, f1, d1
        except:
            return

def update_agent(board):
    info = [ None ] * (AGENT_MINE + 1)
    info[AGENT_TORPEDO] = board.torpedo
    #info[AGENT_SONAR] = board.sonar
    info[AGENT_SILENCE] = board.silence
    info[AGENT_MINE] = board.mine
    return info

def sector(obj1):
    return 1 + (self.x // 5) + ( (self.y // 5) * 3 )

def manhattan(obj1,obj2):
    distance = abs(obj1.x - obj2.x) + abs(obj1.y - obj2.y)
    return distance

def square(obj1,obj2):
    is_true = True
    is_true &= False if abs(obj1.x - obj2.x) > 1 else True
    is_true &= False if abs(obj1.y - obj2.y) > 1 else True
    return is_true

def path_solving(game_board,puzzle):
    puzzle.start = game_board[MY_ID].y , game_board[MY_ID].x

    # TODO: Idea but not finished or not done good result
    if puzzle.finish == None :
        y_row , x_col = puzzle.coord_random()
        puzzle.finish = y_row, x_col

    solution = puzzle.solve()
    return game_board, puzzle, solution

if __name__ == '__main__':
    read_map()
    t_check_map(TREASURE_MAP)
    game_board[MY_ID] = Board(game_board[MY_ID])

    puzzle = HamiltonSolver(None)
    puzzle.set_up(game_board[MY_ID].treasure_map)
    y_row , x_col = puzzle.coord_random()
    puzzle.legal.remove( (y_row,x_col) )
    game_board[MY_ID].x, game_board[MY_ID].y = x_col, y_row
    game_board, puzzle, solution = path_solving(game_board,puzzle)

    kanban_opp = StalkAndTorpedo(None)
    kanban_opp.set_up(TREASURE_MAP)

    kanban_mine = MineAndTrigger(None)
    lambda_n = lambda t1, m1 : '.' if t1 == '.' and m1 == '.' else ' '
    for i1 in range(15):
        MINE_MAP[i1] = [ lambda_n(t1,m1) for t1, m1 in zip(TREASURE_MAP[i1],MINE_MAP[i1]) ]
    kanban_mine.set_up(MINE_MAP)

    print("{} {}".format(game_board[MY_ID].x,game_board[MY_ID].y))

    turn = 1

    while True:
        print("TURN {}".format(turn),file=sys.stderr)
        game_board[MY_ID] = Board(game_board[MY_ID])
        game_board[OPP_ID] = Board(game_board[OPP_ID])
        update(game_board[MY_ID],game_board[OPP_ID])

        if turn == DEEP + 1 :
            puzzle = HamiltonSolver(puzzle)
            game_board, puzzle, solution = path_solving(game_board,puzzle)

            if solution is None :
                # TODO: WARNING : Write a state in this case

                game_board[MY_ID].treasure_map = TREASURE_MAP
                game_board[MY_ID].write_surface()
                puzzle.reset()
                puzzle.legal.remove( (game_board[MY_ID].y,game_board[MY_ID].x) )

            elif len(solution) != (DEEP + 1) :
                # TODO: WARNING : Write a state in this case

                game_board[MY_ID].treasure_map = TREASURE_MAP
                game_board[MY_ID].write_surface()
                puzzle.reset()
                puzzle.legal.remove( (game_board[MY_ID].y,game_board[MY_ID].x) )

            else :
                turn = 1

        if turn == 1 and game_board[MY_ID].silence == 0:
            y_row , x_col = puzzle.read_turn(solution,turn)
            dir = GET_DIRS[ (y_row - game_board[MY_ID].y, x_col - game_board[MY_ID].x)]
            game_board[MY_ID].y, game_board[MY_ID].x = y_row, x_col
            game_board[MY_ID].write_silence(dir,1)
            turn += 1

        #t_check_map(game_board[MY_ID].treasure_map)
        print("Position (y:{},x:{})".format(game_board[MY_ID].y,game_board[MY_ID].x),file=sys.stderr)

        sonar_result = input()
        print(sonar_result, file=sys.stderr)
        opponent_orders = input()

        for c1, f1, d1 in update_order(opponent_orders):
            if f1 is not None:
                kanban_opp.update(f1,d1)
                kanban_opp = StalkAndTorpedo(kanban_opp)

        print("Kanban Board {} Torpedo {}".format(
        len(kanban_opp.inp),game_board[MY_ID].torpedo),file=sys.stderr)

        if game_board[MY_ID].mine == 0 :

            orientation = kanban_mine.mine(game_board[MY_ID])
            if orientation is not None :
                game_board[MY_ID].write_mine(orientation)
                game_board[MY_ID].mine = 3

        if len(kanban_opp.inp) <= SEARCH_OPP_TORPEDO and game_board[MY_ID].torpedo == 0:
            for s1,_ in kanban_opp.inp :
                distance = manhattan(s1,game_board[MY_ID])
                if  distance >= 2 and distance <= 4 :
                    game_board[MY_ID].write_torpedo(s1.x,s1.y)
                    game_board[MY_ID].torpedo = 3
                    break

        if len(kanban_opp.inp) <= SEARCH_OPP_TRIGGER and len(kanban_mine.minefield) > 0 :
            for s1,_ in kanban_opp.inp :
                mine = kanban_mine.nearby(game_board[MY_ID],s1)
                if mine is not None:
                    kanban_mine.trigger(mine)
                    game_board[MY_ID].write_trigger(mine.x,mine.y)
                    break

        info = update_agent(game_board[MY_ID])
        text = ''
        try :
            i1 = next(i1 for i1,agent1 in enumerate(info) if agent1 != 0)
            text = select_a[i1]
        except StopIteration:
            text = 'SONAR'

        if turn > 0 and turn < DEEP + 1 :
            y_row , x_col = puzzle.read_turn(solution,turn)
            dir = GET_DIRS[ (y_row - game_board[MY_ID].y, x_col - game_board[MY_ID].x)]
            game_board[MY_ID].write_move(dir,text)
            turn += 1

        print(game_board[MY_ID].out)
