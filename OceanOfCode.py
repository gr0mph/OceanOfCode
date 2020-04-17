import sys
import math
import copy
import random
import time

TURN_OPP_SILENCE = -1

game_board = [ None , None ]
movement_f = { 'N': None,'S': None,'E': None,'W': None }

state = 0
k_STATE_AGENT_STARTING = 0
k_STATE_AGENT_DISCRETE = 1
k_STATE_AGENT_SEARCHING = 2
k_STATE_AGENT_MINING = 3
k_STATE_AGENT_WARING = 4

print_agent = {
k_STATE_AGENT_STARTING: 'k_STATE_AGENT_STARTING',
k_STATE_AGENT_DISCRETE: 'k_STATE_AGENT_DISCRETE',
k_STATE_AGENT_SEARCHING: 'k_STATE_AGENT_SEARCHING',
k_STATE_AGENT_MINING: 'k_STATE_AGENT_MINING',
k_STATE_AGENT_WARING: 'k_STATE_AGENT_WARING'
}

STATE_MOVE=[
[ 'TORPEDO' , 'SILENCE' , 'MINE' , 'SONAR' ],
[ 'SILENCE' , 'MINE' , 'SONAR' , 'TORPEDO' ],
[ 'SILENCE' , 'SONAR' , 'MINE' , 'TORPEDO' ],
[ 'MINE' , 'SILENCE' , 'TORPEDO' , 'SONAR' ],
[ 'TORPEDO' , 'MINE' , 'SONAR' , 'SILENCE' ],
]
PREVIOUS_SONAR = 0

WIDTH, HEIGHT, MY_ID, OPP_ID = 0 , 0, 0, 0
TREASURE_MAP = []

STARTING_SYMBOLS = 'S'
FINISHING_SYMBOLS = 'F'
OBSTACLE_SYMBOL = 'x'
EMPTY_SYMBOLS = '.'

DIRS = [('N',-1, 0), ('S',1, 0), ('E',0, 1), ('W',0, -1)]
GET_DIRS = { (-1,0) : 'N' , (1,0) : 'S' , (0,1) : 'E' , (0,-1) : 'W' }
OPP_DIRS = { 'N' : ('S',1, 0) , 'S' : ('N',-1, 0) , 'E' : ('W',0, -1) , 'W' : ('E',0, 1) }
OPPONENT_SET = set()

k_PATH_HAMILTON = 1
k_PATH_FIRST = 2
k_PATH_LAST = 3
k_PATH_MAX = 4

# TODO: Can be improved
SECTOR_REDUCING = {
(6,3):(6,3,2,1,4,7,8,9,0),(6,9):(6,9,8,7,4,1,2,3,0),
(8,9):(8,9,6,3,2,1,4,7,0),(8,7):(8,7,4,1,2,3,6,9,0),
(4,7):(4,7,8,9,6,3,2,1,0),(4,1):(4,1,2,3,6,9,8,7,0),
(2,1):(2,1,4,7,8,9,6,3,0),(2,3):(2,3,6,9,8,7,4,1,0)
}

SECTOR_TRANSIT = {
5: (6,8,4,2),6: (3,9),8: (9,7),4: (7,1),2: (1,3),
1: (2,4), 3: (2,6), 7:(4,8), 9:(8,6)
}

SILENCE_NEED_FUSION = 0

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

DEEP_SILENCE2 = 41
SEARCH_OPP_TRIGGER = 3
SEARCH_OPP_TRIGGER_LOT = 11

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
        REDUCE_MAP = solving.grid
        self.privileged_dir = copy.copy(DIRS)
        self.possible_dir = copy.copy(DIRS)
        legal = solving.legal

        results = [dir for dir in DIRS if is_direction_legal(self,legal,dir)]

        coord = self.y, self.x
        length = len(results)

        if len(results) == 0 :
            y_row, x_col = coord
            solving.delete.append(coord)
            REDUCE_MAP[self.y][self.x] = 'x'

        elif length <= 1 :
            y_row, x_col = coord
            d1, y_drow, x_dcol = results[0]
            solving.delete.append(coord)
            coord = y_row + y_drow, x_col + x_dcol
            if coord not in solving.dirunknow :
                solving.dirunknow.append(coord)
            REDUCE_MAP[self.y][self.x] = 'x'

        elif length == 2 :
            self.possible_dir = copy.copy(results)
            self.privileged_dir = None
            solving.risk.append(coord)
            solving.legal.update( { coord : self } )

        else :
            self.possible_dir = copy.copy(results)
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
        self.dirunknow = []
        self.risk = []
        self.delete = []
        self.sector = [None] * 10
        self.last = None
        if clone is not None :
            self.grid = clone.grid
            self.legal = clone.legal
            self.start = clone.start
            self.risk = clone.risk

    def set_up(self,TREASURE_MAP):
        self.grid = copy.copy(TREASURE_MAP)
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
        self.delete.clear()

        for coord in self.dirunknow:
            if coord not in self.legal :
                continue
            n1 = self.legal[coord]
            y_row, x_col = coord
            results = [dir for dir in n1.possible_dir if is_direction_legal(n1,self.legal,dir)]
            n1.possible_dir = results
            if len(n1.possible_dir) <= 2 :
                self.risk.append(coord)
        self.dirunknow.clear()

        for coord in self.risk:
            self.risk.pop(0)
            self.update_risk(coord)

    def update_risk(self,k_coord):
        y_row, x_col = k_coord
        if k_coord not in self.legal:
            self.grid[y_row][x_col] = 'x'
            return

        if len(self.legal[k_coord].possible_dir) == 1 :
            self.grid[y_row][x_col] = 'x'
            del self.legal[k_coord]
            return

        MIN_REQUIRE_DEEP = 6
        soluce = 0

        start_time = time.time()
        r , c = self.legal[k_coord].y, self.legal[k_coord].x
        the_first_node = self.legal[k_coord]

        for d1 in the_first_node.possible_dir:
            direction, y1_drow, x1_dcol = d1
            start = r + y1_drow, c + x1_dcol

            legal = copy.copy(self.legal)
            coord = r , c
            del legal[coord]

            # The next risky cell has been already deleted
            # So we can delete this test and check next
            if start not in legal :
                return

            n1 = legal[start]
            coord = n1.y , n1.x
            del legal[coord]

            path = [n1]
            iter_dir = [iter(n1.possible_dir)]
            iter_delete = [n1]

            path_append = path.append
            path_pop = path.pop
            iter_dir_extend = iter_dir.extend
            iter_dir_append = iter_dir.append
            iter_dir_pop = iter_dir.pop

            while path:
                n1 = path[-1]
                y_row, x_col = n1.y , n1.x
                for d1 in iter_dir[-1]:

                    orientation, y_drow, x_dcol = d1
                    new_coord = y_row + y_drow, x_col + x_dcol

                    if new_coord in legal and len(legal[new_coord].possible_dir) > 0 :
                        n1 = legal[new_coord]
                        path_append(n1)
                        del legal[new_coord]

                        if n1 not in iter_delete:
                            iter_delete.append(n1)
                        iter_dir_append(iter(n1.possible_dir))

                        if len(path) > MIN_REQUIRE_DEEP :
                            soluce += 1

                        # Recompute fucking iter
                        break

                else:
                    iter_dir.pop()
                    n1 = path_pop()
                    coord = n1.y , n1.x
                    legal[coord] = n1

                if len(path) > MIN_REQUIRE_DEEP:
                    break

            if len(path) == 0 :
                for n1 in iter_delete:
                    y_row, x_col = n1.y, n1.x
                    iter_delete_coord = n1.y, n1.x
                    self.grid[y_row][x_col] = 'x'
                    del self.legal[iter_delete_coord]

                d2 = OPP_DIRS[direction]
                risk = the_first_node.y + y1_drow, the_first_node.x + x1_dcol
                if risk in self.legal:
                    self.legal[risk].possible_dir.remove(d2)
                    self.risk.append(risk)
                y_row, x_col = k_coord
                self.grid[y_row][x_col] = 'x'
                del self.legal[k_coord]
                break

    def update_sector(self):
        for i1 in range(0,10):
            self.sector[i1] = {}

        for c1,n1 in self.legal.items():
            sector_id = sector(n1)
            c1 = n1.y, n1.x
            self.sector[sector_id][c1] = n1

    def next_sector(self,path):
        self.last = path[-1]
        k_last_coord = self.last.y, self.last.x
        k_last_sector = sector(self.last)
        del self.sector[k_last_sector][k_last_coord]

    def solve_sector(self,next_sector):
        save = []
        max_find = False
        first_find = False
        save_type = 0
        for type, path in self.solve(next_sector):
            if type == k_PATH_HAMILTON :
                save_type = type
                save = path
                break

            if type == k_PATH_MAX :
                max_find = True
                save_type = type
                save = copy.copy(path)

            if max_find == False and type == k_PATH_FIRST :
                first_find = True
                save_type = type
                save = copy.copy(path)  # This data is ephemerate

            if max_find == False and first_find == False and type == k_PATH_LAST :
                save_type = type
                save = copy.copy(path)  # This data is ephemerate

        return save_type, save

    def coord_random(self):
        node = random.choice(list(self.legal))
        return node

    def read_turn(self,path,turn):
        return path[turn]

    def solve(self,sector_end):
        y_row, x_col = self.last.y, self.last.x
        sector_start = sector(self.last)
        k_coord = y_row, x_col

        SECTOR_DEEP = len(self.sector[sector_start])
        DISTANCE_PATH = 0

        n1 = self.last
        coord1 = n1.y , n1.x
        d1 = n1.possible_dir

        path = [n1]
        iter_dir = [iter(n1.possible_dir)]

        path_append = path.append
        path_pop = path.pop
        iter_dir_extend = iter_dir.extend
        iter_dir_append = iter_dir.append
        iter_dir_pop = iter_dir.pop
        first = 0

        search_path_max = 10
        search_path = None

        while path:
            n1 = path[-1]
            y_row, x_col = n1.y , n1.x
            for d1 in iter_dir[-1]:

                orientation, y_drow, x_dcol = d1
                new_coord = y_row + y_drow, x_col + x_dcol
                if new_coord in self.sector[sector_start] :
                    n1 = self.sector[sector_start][new_coord]
                    path_append(n1)
                    del self.sector[sector_start][new_coord]

                    if len(self.sector[sector_start]) == 0 :
                        yield (k_PATH_LAST,path)

                    iter_dir_append(iter(n1.possible_dir))
                    # Recompute fucking iter
                    break

                for k_end in sector_end:
                    if new_coord in self.sector[k_end] and len(self.sector[sector_start]) == 0 :
                        y_row, x_col = new_coord
                        n1 = self.sector[k_end][new_coord]
                        path_append(n1)
                        yield (k_PATH_HAMILTON, path)
                        return

                    if new_coord in self.sector[k_end] and first == 0:
                        first = 1
                        path_append(self.sector[k_end][new_coord])
                        yield (k_PATH_FIRST, path)
                        path_pop()

                    if new_coord in self.sector[k_end] and len(path) > search_path_max :
                        search_path = copy.copy(path)
                        search_path.append(self.sector[k_end][new_coord])
                        search_path_max = len(search_path)

            else:
                iter_dir.pop()
                n1 = path_pop()
                coord = n1.y , n1.x
                self.sector[sector_start][coord] = n1

        if search_path_max > 10 :
            yield (k_PATH_MAX, search_path)

class LegalTorpedo():

    def __init__(self,clone):
        self.reducing_map = None
        self.legal = set()

    def set_up(self,REDUCING_MAP):
        self.reducing_map = REDUCING_MAP
        for y_row, row in enumerate(self.reducing_map):
            for x_col, item in enumerate(row):
                if item in EMPTY_SYMBOLS:
                    self.legal.add( (y_row, x_col) )

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
            self.legal = copy.copy(clone.legal)

    def __str__(self):
        text = ''
        for y_row, x_col in self.legal:
            text = '{} ({},{})'.format(text,x_col,y_row)
        return text

    def set_up(self,TREASURE_MAP):
        i1 = 0
        for y_row, row in enumerate(TREASURE_MAP):
            for x_col, item in enumerate(row):
                if item in EMPTY_SYMBOLS:
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
        if new_coord in self.legal:
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

# In fact, it's the second method
STALKING_SILENCE = {
'E':( (-4,0),(-3,0),(-2,0),(-1,0),(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0),(4,0) ),
'W':( (-4,0),(-3,0),(-2,0),(-1,0),(0,-1),(0,-2),(0,-3),(0,-4),(1,0),(2,0),(3,0),(4,0) ),
'N':( (0,-1),(0,-2),(0,-3),(0,-4),(-4,0),(-3,0),(-2,0),(-1,0),(0,1),(0,2),(0,3),(0,4) ),
'S':( (0,-1),(0,-2),(0,-3),(0,-4),(4,0),(3,0),(2,0),(1,0),(0,1),(0,2),(0,3),(0,4) )
}

# With DICTIONNARY, LIST, TUPLE of TUPLE
STALKING_SILENCE3 = {
'E':[
( (-1,0),(-2,0),(-3,0),(-4,0) ),
( (0,1),(0,2),(0,3),(0,4) ),
( (1,0),(2,0),(3,0),(4,0) )
],
'W':[
( (-1,0),(-2,0),(-3,0),(-4,0) ),
( (0,-1),(0,-2),(0,-3),(0,-4) ),
( (1,0),(2,0),(3,0),(4,0) )
],
'N':[
( (0,-1),(0,-2),(0,-3),(0,-4) ),
( (-1,0),(-2,0),(-3,0),(-4,0) ),
( (0,1),(0,2),(0,3),(0,4) )
],
'S':[
( (0,-1),(0,-2),(0,-3),(0,-4) ),
( (1,0),(2,0),(3,0),(4,0) ),
( (0,1),(0,2),(0,3),(0,4) )
]
}

STALKING_SILENCE_SECTOR = {
(0,'E') : (1,2,3,4,5,6,7,8,9) , (1,'E') : (2,3,5,6,8,9) , (2,'E') : (3,6,9) ,
(0,'W') : (1,2,3,4,5,6,7,8,9) , (1,'W') : (1,2,4,5,7,8) , (2,'W') : (1,4,7) ,
(0,'N') : (1,2,3,4,5,6,7,8,9) , (1,'N') : (1,2,3,4,5,6) , (2,'N') : (1,2,3) ,
(0,'S') : (1,2,3,4,5,6,7,8,9) , (1,'S') : (4,5,6,7,8,9) , (2,'S') : (7,8,9)
}

class StalkAndTorpedo():

    def __init__(self,clone):
        self.treasure_map = None
        self.out = set()
        self.inp = set()
        self.previous_move = ''
        self.previous_nb = 0
        if clone is not None :
            self.treasure_map, self.inp = clone.treasure_map, clone.out
            self.previous_move = clone.previous_move
            self.previous_nb = clone.previous_nb

    def __str__(self):
        text = ''
        for board_in, stalk_in in self.inp:
            text = '{}\n({},{},life{})'.format(text,board_in.x, board_in.y, board_in.life)
        return text

    def set_up(self,tuple_sector,TREASURE_MAP):
        inp_add = self.inp.add
        new_board, new_stalk = None, None
        self.treasure_map = TREASURE_MAP
        for y_row, row in enumerate(self.treasure_map):
            for x_col, item in enumerate(row):

                sector = 1 + (x_col // 5) + ( (y_row // 5) * 3 )
                if sector not in tuple_sector :
                    continue

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
        self.previous_nb = (self.previous_nb + 1) if (self.previous_move == d) else 0
        self.previous_move = d
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
                #board.treasure_map = copy.deepcopy(TREASURE_MAP)
                board.treasure_map = copy.copy(TREASURE_MAP)
                stalk.read_surface(board)
                self.out.add( (board,stalk) )

    def read_surface2(self,data):
        print("Read surface 2 {}".format(int(data[0])),file=sys.stderr)
        for board, stalk in self.inp:
            if int(data[0]) == sector(board):
                #board.treasure_map = copy.deepcopy(TREASURE_MAP)
                board.treasure_map = copy.copy(TREASURE_MAP)
                stalk.read_surface(board)
                self.out.add( (board,stalk) )

    def read_torpedo(self,data):
        x, y = int(data[0]), int(data[1])
        point = Point(x,y)
        for board, stalk in self.inp:
            distance = manhattan(board,point)
            if distance <= 4 :
                self.out.add( (board,stalk) )

    def read_silence2(self,data):
        global SILENCE_NEED_FUSION
        inp = self.inp
        out_add = self.out.add
        if len(self.inp) >= DEEP_SILENCE2:
            SILENCE_NEED_FUSION = 0
            self.inp.clear()

            identical_movement_number = self.previous_nb // 5
            tuple_sector = STALKING_SILENCE_SECTOR[(identical_movement_number,self.previous_move)]

            self.set_up(tuple_sector,self.treasure_map)
            self.out = self.inp

        else :
            SILENCE_NEED_FUSION = 1
            for board, stalk in inp:
                out_add( (board, stalk))

                t_stalking_silence = STALKING_SILENCE3[self.previous_move]
                for tuple_dir in t_stalking_silence:
                    for y_drow,x_dcol in tuple_dir:
                        k_coord = board.y + y_drow, board.x + x_dcol
                        if k_coord in stalk.legal :
                            board1, stalk1 = Board(board), StalkAndLegal(stalk)
                            board1.y += y_drow
                            board1.x += x_dcol
                            out_add( (board1,stalk1) )
                        else :
                            break

    def silence_fusion(self):
        inp = self.inp
        dico_coord = {}
        out_add = self.out.add

        for board, stalk in inp:
            k_coord = board.y , board.x
            if k_coord in dico_coord :
                dico_coord[k_coord].append( (board, stalk) )
            else:
                dico_coord[k_coord] = [ (board,stalk) ]

        for k_coord, d1 in dico_coord.items():
            board, stalk = None, StalkAndLegal(None)
            legal_add = stalk.legal.add
            for board1,stalk1 in d1:
                if board == None:
                    board = board1

                for coord1 in stalk1.legal:
                    legal_add(coord1)

            out_add( (board,stalk) )

    def update_sonar(self,sonar_result,previous):
        if sonar_result == 'Y':
            for board, stalk in self.inp:
                if previous == sector(board):
                    board.treasure_map = copy.copy(TREASURE_MAP)
                    stalk.read_surface(board)
                    self.out.add( (board,stalk) )
        else:
            for board, stalk in self.inp:
                if previous != sector(board):
                    board.treasure_map = copy.copy(TREASURE_MAP)
                    stalk.read_surface(board)
                    self.out.add( (board,stalk) )

READ_COMMAND = [
( 'MOVE' , StalkAndTorpedo.read_move ),
( 'SURFACE' , StalkAndTorpedo.read_surface2 ),
( 'TORPEDO' , StalkAndTorpedo.read_torpedo ),
( 'SONAR' , None ),
( 'SILENCE' , StalkAndTorpedo.read_silence2 ),
( 'MINE' , None ),
( 'TRIGGER' , None ),
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
MINE_MAP.append(list('    .     .    '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('  .    .    .  '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list('    .     .    '))
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

    def write_sonar(self,sector):
        t = f'SONAR {sector}'
        self.out = t if self.out == '' else f'{self.out} | {t}'

    def order(self):
        print(self.out)

class Board(Submarine):

    def __init__(self,clone):
        super().__init__(clone)
        self.turn = 0
        self.x , self.y , self.life = 0, 0, 6
        self.torpedo, self.sonar, self.silence, self.mine = 0, 0, 0, 0

        self.need_surface = False
        self.legal_torpedo = None
        self.unknow_opp = True
        self.nearest = False

        if clone is not None:
            self.turn = clone.turn + 1
            self.x, self.y, self.life = clone.x, clone.y, clone.life
            self.torpedo, self.sonar = clone.torpedo, clone.sonar
            self.silence, self.mine = clone.silence, clone.mine
            self.need_surface = clone.need_surface
            self.legal_torpedo = clone.legal_torpedo # Only not lost link
            self.unknow_opp = clone.unknow_opp
            self.nearest = clone.nearest

    def __str__(self):
        return '({},{})'.format(self.x,self.y)


def update(me,opp):
    me.x, me.y, me.life, opp.life, me.torpedo, me.sonar, me.silence, me.mine = [int(i) for i in input().split()]

def update_order(text):
    text, t1 = text.split('|'), ''
    for t1 in text:
        try:
            c1, f1 = next( (c1,f1) for c1,f1 in READ_COMMAND if t1.find(c1) != -1 )
            t_list = t1.split(' ')
            _,d1 = t_list[0], t_list[1:]
            yield c1, f1, d1
        except:
            return

def update_agent(state,board):
    STATE_CHECK = {
    'SILENCE' : board.silence, 'SONAR' : board.sonar,
    'TORPEDO' : board.torpedo, 'MINE' : board.mine
    }
    info = STATE_MOVE[state]
    text = ''
    try:
        text = next(n1 for n1 in info if STATE_CHECK[n1] != 0)
    except:
        text = 'TORPEDO'
    return text

def sector(obj1):
    return 1 + (obj1.x // 5) + ( (obj1.y // 5) * 3 )

def manhattan(obj1,obj2):
    distance = abs(obj1.x - obj2.x) + abs(obj1.y - obj2.y)
    return distance

def square(obj1,obj2):
    if abs(obj1.x - obj2.x) > 1 :
        return False

    if abs(obj1.y - obj2.y) > 1 :
        return False

    return True

def square2(mine,my_board,opp_board):
    if square(my_board,mine) == True :
        return False

    if square(opp_board,mine) == True :
        return True

    return False

def average_x( triple_x , obj1 ):
    min_x, ave_x, max_x = triple_x
    min_x = min(min_x, obj1.x)
    max_x = max(max_x, obj1.x)
    ave_x = ave_x + obj1.x
    return (min_x, ave_x, max_x)

def average_y( triple_y , obj1 ):
    min_y, ave_y, max_y = triple_y
    min_y = min(min_y, obj1.y)
    max_y = max(max_y, obj1.y)
    ave_y = ave_y + obj1.y
    return (min_y, ave_y, max_y)


OBSERVER_TORPEDO = ( (-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1) )
BOARD_OBSERVER_TORPEDO = (
(-4,0),
(-3,-1),(-3,0),(-3,1),
(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),
(-1,-3),(-1,-2),(-1,2),(-1,3),
(0,-4),(0,-3),(0,-2),(0,2),(0,3),(0,4),
(1,-3),(1,-2),(1,2),(1,3),
(2,-2),(2,-1),(2,0),(2,1),(2,2),
(3,-1),(3,0),(3,1),
(4,0)
)

class TorpedoObserver():

    def __init__(self,clone):
        self.me = True
        self.dict_torpedo = {}
        for y_drow, x_dcol in BOARD_OBSERVER_TORPEDO:
            self.dict_torpedo[(y_drow, x_dcol)] = 0
        self.torpedo = (-1,-1)

    def __str__(self):
        y, x = self.torpedo
        return f'Torpedo Obs: ({y},{x})'

    def reset(self):
        for y_drow, x_dcol in BOARD_OBSERVER_TORPEDO:
            self.dict_torpedo[(y_drow, x_dcol)] = 0
        self.torpedo = (-1,-1)

    def notify_iter(self,submarine,kanban_mine,k_board_opp,k_stalk_opp):
        distance = manhattan(submarine,k_board_opp)
        if distance > 5 :
            pass
        else :
            y_diff = k_board_opp.y - submarine.y
            x_diff = k_board_opp.x - submarine.x

            if (y_diff,x_diff) in self.dict_torpedo:
                self.dict_torpedo[(y_diff,x_diff)] += 6

            for y_drow, x_dcol in OBSERVER_TORPEDO:

                y_diff_drow,x_diff_dcol = y_diff + y_drow, x_diff + x_dcol

                y1_ = k_board_opp.y + y_drow
                x1_ = k_board_opp.x + x_dcol
                if (y1_,x1_) not in submarine.legal_torpedo.legal :
                    continue

                if (y_diff_drow,x_diff_dcol) in self.dict_torpedo :
                    if self.dict_torpedo[(y_diff_drow,x_diff_dcol)] == 0 and distance == 5 :
                        continue
                    self.dict_torpedo[(y_diff_drow,x_diff_dcol)] += 1
        return True

    def notify_else(self,submarine,kanban_mine,kanban_opp):
        y_drow,x_dcol = max(self.dict_torpedo, key = self.dict_torpedo.get)

        if self.dict_torpedo[(y_drow,x_dcol)] > 0 :
            y_row, x_col = submarine.y + y_drow, submarine.x + x_dcol
            submarine.write_torpedo(x_col,y_row)
            submarine.torpedo = 3
            self.torpedo = (y_row,x_col)
            return True

        else :
            return False

    def notify_check(self,submarine,kanban_mine,kanban_opp):
        k_coord = self.torpedo
        y_torpedo, x_torpedo = k_coord

        if submarine.torpedo == 0 :
            # Torpedo has failed
            print("Torpedo fail: {} --> no update".format(self),file=sys.stderr)
            print("Len Kanban Opp: {}".format(len(kanban_opp.inp)),file=sys.stderr)
            return False

        if self.lost_life == 0:
            all_set = set()
            all_set.add(k_coord)
            for y_drow, x_dcol in OBSERVER_TORPEDO:
                y_diff_drow,x_diff_dcol = y_torpedo + y_drow, x_torpedo + x_dcol
                all_set.add( (y_diff_drow,x_diff_dcol) )

            for board,stalk in kanban_opp.inp:
                board_coord = board.y, board.x
                if board_coord not in all_set:
                    kanban_opp.out.add( (board,stalk) )

            return True

        elif self.nb_observer_check == 1 :

            if self.lost_life == 1:
                all_set = set()
                for y_drow, x_dcol in OBSERVER_TORPEDO:
                    y_diff_drow,x_diff_dcol = y_torpedo + y_drow, x_torpedo + x_dcol
                    all_set.add( (y_diff_drow,x_diff_dcol) )

                for board,stalk in kanban_opp.inp:
                    board_coord = board.y, board.x
                    if board_coord in all_set:
                        kanban_opp.out.add( (board,stalk) )
                return True

            elif self.lost_life == 2:
                all_set = set()
                all_set.add(k_coord)

                for board,stalk in kanban_opp.inp:
                    board_coord = board.y, board.x
                    if board_coord in all_set:
                        kanban_opp.out.add( (board,stalk) )
                return True
        return False

class TriggerObserver():

    def __init__(self,clone):
        #
        self.me = True
        self.dict_mine = {}
        self.trigger = (-1,-1)

    def __str__(self):
        y, x = self.trigger
        return f'Trigger Obs: ({y},{x})'

    def reset(self):
        self.dict_mine = {}
        self.trigger = (-1,-1)

    def notify_iter(self,submarine,kanban_mine,k_board_opp,k_stalk_opp):
        list_mine = [mine for mine in kanban_mine.minefield if square2(mine,submarine,k_board_opp)]
        for m1 in list_mine:
            if m1 in self.dict_mine:
                if m1.y == k_board_opp.y and m1.x == k_board_opp.x :
                    self.dict_mine[m1] += 6
                else :
                    self.dict_mine[m1] += 1
            else :
                if m1.y == k_board_opp.y and m1.x == k_board_opp.x :
                    self.dict_mine[m1] = 6
                else :
                    self.dict_mine[m1] = 1
        return True

    def notify_else(self,submarine,kanban_mine,kanban_opp):
        mine = max(self.dict_mine, key = self.dict_mine.get,default=None)

        if mine == None :
            return False

        if self.dict_mine[mine] > 0 :
            submarine.write_trigger(mine.x,mine.y)
            submarine.mine = 3
            kanban_mine.trigger(mine)
            self.trigger = (mine.y,mine.x)
            return True

        else :
            return False

    def notify_check(self,submarine,kanban_mine,kanban_opp):
        k_coord = self.trigger
        y_torpedo, x_torpedo = k_coord

        if self.lost_life == 0:
            all_set = set()
            all_set.add(k_coord)
            for y_drow, x_dcol in OBSERVER_TORPEDO:
                y_diff_drow,x_diff_dcol = y_torpedo + y_drow, x_torpedo + x_dcol
                all_set.add( (y_diff_drow,x_diff_dcol) )

            for board,stalk in kanban_opp.inp:
                board_coord = board.y, board.x
                if board_coord not in all_set:
                    kanban_opp.out.add( (board,stalk) )

            return True

        elif self.nb_observer_check == 1 :

            if self.lost_life == 1:
                all_set = set()
                for y_drow, x_dcol in OBSERVER_TORPEDO:
                    y_diff_drow,x_diff_dcol = y_torpedo + y_drow, x_torpedo + x_dcol
                    all_set.add( (y_diff_drow,x_diff_dcol) )

                for board,stalk in kanban_opp.inp:
                    board_coord = board.y, board.x
                    if board_coord in all_set:
                        kanban_opp.out.add( (board,stalk) )
                return True

            elif self.lost_life == 2:
                all_set = set()
                all_set.add(k_coord)

                for board,stalk in kanban_opp.inp:
                    board_coord = board.y, board.x
                    if board_coord in all_set:
                        kanban_opp.out.add( (board,stalk) )
                return True
        return False

class SonarObserver():

    def __init__(self,clone):
        #
        self.nb_sector = [ 0 ] * 10
        self.sonar = 0
        pass

    def __str__(self):
        sonar = self.sonar
        return f'Sonar {sonar}'

    def reset(self):
        self.nb_sector = [ 0 ] * 10
        self.sonar = 0
        pass

    def notify_iter(self,submarine,kanban_mine,k_board_opp,k_stalk_opp):
        # TODO
        self.nb_sector[sector(k_board_opp)] += 1
        return True

    def notify_else(self,submarine,kanban_mine,kanban_opp):
        m = max(self.nb_sector)
        nb_solution = 0
        # Check One solution or Two solution,etc.
        for i1, j1 in enumerate(self.nb_sector):
            if j1 == 0 :
                continue
            nb_solution += 1
            if j1 == m :
                self.sonar = i1

        if nb_solution > 1 :
            submarine.write_sonar(self.sonar)
        else :
            self.reset()
        return False

    def notify_check(self,submarine,kanban_mine,kanban_opp):
        return False

class ObserverQueue():

    def __init__(self,clone):
        self.observer = []
        self.lost_life = 0
        self.nb_observer_check = 0
        pass

    def attach(self,instance):
        self.observer.append(instance)

    def detach(self,instance):
        self.observer.remove(instance)

    def reset(self):
        for instance in self.observer:
            instance.reset()
        self.observer.clear()
        self.lost_life = 0

    def iterator(self,submarine_mine,kanban_opp,kanban_mine):
        length = len(kanban_opp.inp)

        min_x, ave_x, max_x = 14, 0, 0
        min_y, ave_y, max_y = 14, 0, 0

        i1 = 0

        for k_board_opp, k_stalk_opp in kanban_opp.inp:

            instance, success = None, False
            for instance in self.observer:
                success = instance.notify_iter(submarine_mine,kanban_mine,k_board_opp,k_stalk_opp)

            min_x, ave_x, max_x = average_x( (min_x, ave_x, max_x), k_board_opp )
            min_y, ave_y, max_y = average_y( (min_y, ave_y, max_y), k_board_opp )

            print("({},{}) _ ".format(k_board_opp.x,k_board_opp.y),file=sys.stderr,end="")
            i1 += 1
            if i1 == 5 :
                print("",file=sys.stderr)
                i1 = 0

        print("",file=sys.stderr)

        ave_x = ave_x // len(kanban_opp.inp)
        ave_y = ave_y // len(kanban_opp.inp)

        check_confined = (max_x - min_x) + (max_y - min_y)
        submarine_mine.unknow_opp = False if check_confined <= 6 else True
        print("Check confined {} max ({},{}) min ({},{}) diff ({},{})".format(
            check_confined, max_x,max_y,min_x,min_y,(max_x-min_x),(max_y-min_y)),file=sys.stderr)

        check_nearest = abs(ave_x - submarine_mine.x) + abs(ave_y - submarine_mine.y)
        print("Check nearest {} me ({},{}) average ({},{})".format(
            check_nearest, submarine_mine.x, submarine_mine.y, ave_x, ave_y), file=sys.stderr)
        submarine_mine.nearest = True if check_nearest <= 7 else False

        success = False

        to_detach = {}
        for i1,instance in enumerate(self.observer):
            success = instance.notify_else(submarine_mine,kanban_mine,kanban_opp)

            if success == False :
                to_detach[i1] = instance

        for i1,instance in to_detach.items():
            self.observer.remove(instance)


    def update(self,submarine_opp,submarine_mine,kanban_opp,kanban_mine):
        for instance in self.observer:
            if instance.me == True :
                instance.lost_life = self.lost_life
                instance.nb_observer_check = self.nb_observer_check
                success = instance.notify_check(submarine_mine,kanban_mine,kanban_opp)
                if success == False :
                    pass
                else :
                    kanban_opp = StalkAndTorpedo(kanban_opp)

        # Remove observer
        self.reset()

        # New kanban opp with new reference
        return kanban_opp

class Planning():

    def __init__(self,clone):
        self.forward = None
        self.index = 0
        self.is_forward = True


    def __next__(self):
        distance = 0
        if self.is_forward == True and self.index != self.last :
            self.index += 1
            distance = self.last - self.index

        elif self.is_forward == True and self.index == self.last :
            self.index -= 1
            distance = self.index
            self.is_forward = False

        elif self.is_forward == False and self.index != 0 :
            self.index -= 1
            distance = self.index

        elif self.is_forward == False and self.index == 0 :
            self.index += 1
            distance = self.index
            self.is_forward = True

        return (distance, self.forward[self.index])

    @property
    def last(self):
        return len(self.forward) - 1

class StrategyStarting():

    def __init__(self,clone):
        self.previous_sector = 5
        self.previous_sector_a, self.previous_sector_b = 0, 0
        self.iter_sector_reducing, self.sector_next = None, -1
        self.turn = 0
        self.agent = k_STATE_AGENT_STARTING
        self.torpedo_obs = None
        self.trigger_obs = None
        self.sonar_obs = None
        pass

    def set_up(self,kanban_path,TREASURE_MAP):
        #print("TREASURE_MAP",file=sys.stderr)
        #for t_r in TREASURE_MAP:
        #    print(t_r,file=sys.stderr)

        kanban_path.set_up(TREASURE_MAP)
        kanban_path.update()

        REDUCE_MAP = kanban_path.grid

        #print("REDUCE_MAP",file=sys.stderr)
        #for t_r in REDUCE_MAP:
        #    print(t_r,file=sys.stderr)

        kanban_path.update_sector()

        coord, kanban_path.last = next(iter(kanban_path.sector[self.previous_sector].items()))
        del kanban_path.sector[5][coord]

        path_reducing = []
        path_reducing.append(kanban_path.last)

        for i in range(9):
            path_reducing = self.path(kanban_path,path_reducing)

        return path_reducing

    def path(self,kanban_path,path_reducing):
        if self.sector_next == 0 :
            pass

        elif self.sector_next == -1:
            k_next_tuple = SECTOR_TRANSIT[self.previous_sector]
            type, result = kanban_path.solve_sector(k_next_tuple)
            path_reducing.extend(result[1:])
            kanban_path.next_sector(path_reducing)
            if type == k_PATH_LAST :
                # PERDU pour PERDU
                self.sector_next = 0

            elif self.previous_sector_a == 0:
                self.previous_sector = self.previous_sector_a = sector(path_reducing[-1])
            else :
                self.previous_sector = self.previous_sector_b = sector(path_reducing[-1])
                t_sector_reducing = (self.previous_sector_a,self.previous_sector_b)
                self.iter_sector_reducing = iter(SECTOR_REDUCING[t_sector_reducing])
                next(self.iter_sector_reducing)
                self.sector_next = next(self.iter_sector_reducing)

        else :
            self.sector_next = next(self.iter_sector_reducing)
            type, result = kanban_path.solve_sector([self.sector_next])
            path_reducing.extend(result[1:])
            kanban_path.next_sector(path_reducing)
            if type == k_PATH_LAST :
                # PERDU pour PERDU
                self.sector_next = 0

        return path_reducing

    def movement(self, submarine, kanban_path, planning):
        self.turn += 1

        if submarine.silence == 0 :
            distance, p1_next = planning.__next__()
            y_row, x_col = p1_next.y, p1_next.x
            dir = GET_DIRS[ (y_row - submarine.y, x_col - submarine.x)]
            submarine.y, submarine.x = y_row, x_col
            submarine.write_silence(dir,1)

            distance, p1_next = planning.__next__()
            return (True, p1_next)

        else :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True
            return (False, p1_next)

    def selection(self,submarine_opp, submarine_mine, kanban_opp, kanban_mine, observer):
        return

class StrategyDiscrete():

    def __init__(self,clone):
        self.turn = 0
        self.agent = k_STATE_AGENT_DISCRETE
        self.torpedo_obs = None
        self.trigger_obs = None
        self.sonar_obs = None

        if clone is not None :
            self.turn = clone.turn
            self.torpedo_obs = clone.torpedo_obs
            self.trigger_obs = clone.trigger_obs
            self.sonar_obs = clone.sonar_obs

    def movement(self, submarine, kanban_path, planning):
        self.turn += 1

        if submarine.silence == 0 and submarine.mine == 0 :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True
                return (False, p1_next)

            y_row, x_col = p1_next.y, p1_next.x
            dir = GET_DIRS[ (y_row - submarine.y, x_col - submarine.x)]
            submarine.y, submarine.x = y_row, x_col
            submarine.write_silence(dir,1)

            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True
            return (True, p1_next)

        else :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True
            return (False, p1_next)

    def selection(self,submarine_opp, submarine_mine, kanban_opp, kanban_mine, observer):

        nb_mine = len(kanban_mine.minefield)

        # Reflexion about TRIGGER
        if nb_mine > SEARCH_OPP_TRIGGER_LOT :
            observer.attach(self.trigger_obs)

        # Reflexion about TORPEDO

        # Reflexion about SONAR
        if submarine_mine.unknow_opp == True and submarine_mine.sonar == 0 :
            observer.attach(self.sonar_obs)

class StrategySearching():

    def __init__(self,clone):
        self.turn = 0
        self.agent = k_STATE_AGENT_SEARCHING
        self.torpedo_obs = None
        self.trigger_obs = None
        self.sonar_obs = None

        if clone is not None :
            self.turn = clone.turn
            self.torpedo_obs = clone.torpedo_obs
            self.trigger_obs = clone.trigger_obs
            self.sonar_obs = clone.sonar_obs


    def movement(self, submarine, kanban_path, planning):
        if submarine.silence == 0 and submarine.sonar == 0 :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True
                return (False, p1_next)

            y_row, x_col = p1_next.y, p1_next.x
            dir = GET_DIRS[ (y_row - submarine.y, x_col - submarine.x)]
            submarine.y, submarine.x = y_row, x_col
            submarine.write_silence(dir,1)

            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True
            return (True, p1_next)

        else :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True
            return (False, p1_next)

    def selection(self,submarine_opp, submarine_mine, kanban_opp, kanban_mine, observer):

        nb_mine = len(kanban_mine.minefield)

        # Reflexion about TRIGGER
        if nb_mine > SEARCH_OPP_TRIGGER_LOT :
            observer.attach(self.trigger_obs)

        # Reflexion about TORPEDO

        # Reflexion about SONAR
        if submarine_mine.sonar == 0 :
            observer.attach(self.sonar_obs)
        pass

class StrategyMining():

    def __init__(self, clone):
        self.turn = 0
        self.agent = k_STATE_AGENT_MINING
        self.torpedo_obs = None
        self.trigger_obs = None
        self.sonar_obs = None

        if clone is not None :
            self.turn = clone.turn
            self.torpedo_obs = clone.torpedo_obs
            self.trigger_obs = clone.trigger_obs
            self.sonar_obs = clone.sonar_obs


    def movement(self, submarine, kanban_path, planning):
        # In case of MINING and TORPEDO is full
        if submarine.silence == 0 :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True
                return (False, p1_next)

            y_row, x_col = p1_next.y, p1_next.x
            dir = GET_DIRS[ (y_row - submarine.y, x_col - submarine.x)]
            submarine.y, submarine.x = y_row, x_col
            submarine.write_silence(dir,1)

            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True
            return (True, p1_next)

        else :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True

            return (False, p1_next)

    def selection(self,submarine_opp, submarine_mine, kanban_opp, kanban_mine, observer):

        nb_mine = len(kanban_mine.minefield)

        # Reflexion about TRIGGER
        if submarine_mine.unknow_opp == False and nb_mine > 0 :
            observer.attach(self.trigger_obs)

        elif nb_mine > SEARCH_OPP_TRIGGER_LOT :
            observer.attach(self.trigger_obs)

        # Reflexion about TORPEDO
        if submarine_mine.torpedo == 0 :
            observer.attach(self.torpedo_obs)

        pass


class StrategyWaring():

    def __init__(self, clone):
        self.turn = 0
        self.agent = k_STATE_AGENT_WARING
        self.torpedo_obs = None
        self.trigger_obs = None
        self.sonar_obs = None

        if clone is not None :
            self.turn = clone.turn
            self.torpedo_obs = clone.torpedo_obs
            self.trigger_obs = clone.trigger_obs
            self.sonar_obs = clone.sonar_obs


    def movement(self, submarine, kanban_path, planning):
        # In case of MINING and TORPEDO is full
        if submarine.silence == 0 :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                planning.is_forward = False if planning.is_forward else True
                submarine.need_surface = True
                return (False, p1_next)

            y_row, x_col = p1_next.y, p1_next.x
            dir = GET_DIRS[ (y_row - submarine.y, x_col - submarine.x)]
            submarine.y, submarine.x = y_row, x_col
            submarine.write_silence(dir,1)

            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True
            return (True, p1_next)

        else :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.need_surface = True

            return (False, p1_next)

    def selection(self,submarine_opp, submarine_mine, kanban_opp, kanban_mine, observer):

        nb_mine = len(kanban_mine.minefield)

        # Reflexion about TRIGGER
        if submarine_mine.unknow_opp == False and nb_mine > 0 :
            observer.attach(self.trigger_obs)

        elif submarine_mine.nearest == True and nb_mine > SEARCH_OPP_TRIGGER :
            observer.attach(self.trigger_obs)

        elif nb_mine > SEARCH_OPP_TRIGGER_LOT :
            observer.attach(self.trigger_obs)

        # Reflexion about TORPEDO
        if submarine_mine.torpedo == 0 :
            observer.attach(self.torpedo_obs)

        # Reflexion about SONAR
        if submarine_mine.sonar == 0 :
            observer.attach(self.sonar_obs)
        pass

if __name__ == '__main__':
    read_map()

    g_strategy_state = StrategyStarting(None)
    kanban_path  = PathSolving(None)
    kanban_plan = Planning(None)

    REDUCE_MAP = copy.deepcopy(TREASURE_MAP)
    kanban_plan.forward = g_strategy_state.set_up(kanban_path,REDUCE_MAP)
    REDUCE_MAP = kanban_path.grid

    kanban_path.update_sector()

    # Legal Torpedo
    legal_torpedo = LegalTorpedo(None)
    legal_torpedo.set_up(REDUCE_MAP)

    game_board[MY_ID] = Board(game_board[MY_ID])
    game_board[MY_ID].legal_torpedo = legal_torpedo

    kanban_opp = StalkAndTorpedo(None)
    kanban_opp.set_up( (1,2,3,4,5,6,7,8,9) , TREASURE_MAP)

    kanban_mine = MineAndTrigger(None)
    lambda_n = lambda t1, m1 : '.' if t1 == '.' and m1 == '.' else ' '
    for i1 in range(15):
        MINE_MAP[i1] = [ lambda_n(t1,m1) for t1, m1 in zip(TREASURE_MAP[i1],MINE_MAP[i1]) ]
    kanban_mine.set_up(MINE_MAP)

    turn = 1
    choice = 0

    print("{} {}".format(kanban_plan.forward[0].x,kanban_plan.forward[0].y))

    TURN_MY_SILENCE = 0

    torpedo_obs = TorpedoObserver(None)
    trigger_obs = TriggerObserver(None)
    torpedo_opp = TorpedoObserver(None)
    torpedo_opp.me = False
    trigger_opp = TriggerObserver(None)
    trigger_opp.me = False
    sonar_obs = SonarObserver(None)

    _observer = ObserverQueue(None)

    g_strategy_state.torpedo_obs = torpedo_obs
    g_strategy_state.trigger_obs = trigger_obs
    g_strategy_state.sonar_obs = sonar_obs

    while True:

        game_board[MY_ID] = Board(game_board[MY_ID])
        game_board[OPP_ID] = Board(game_board[OPP_ID])

        MY_LOST_LIFE = game_board[MY_ID].life
        OPP_LOST_LIFE = game_board[OPP_ID].life
        update(game_board[MY_ID],game_board[OPP_ID])
        print("Submarine Me: ({},{})".format(game_board[MY_ID].x,game_board[MY_ID].y),file=sys.stderr)
        MY_LOST_LIFE -= game_board[MY_ID].life
        OPP_LOST_LIFE -= game_board[OPP_ID].life

        p1_next = None
        need_surface = 0

        _, p1_next = g_strategy_state.movement(game_board[MY_ID], kanban_path, kanban_plan)

        sonar_result = input()
        if sonar_obs.sonar != 0 :
            kanban_opp.update_sonar(sonar_result,sonar_obs.sonar)
            kanban_opp = StalkAndTorpedo(kanban_opp)
            sonar_obs.reset()

        opponent_orders = input()

        _observer.lost_life = OPP_LOST_LIFE
        _observer.nb_observer_check = len(_observer.observer)
        if "SURFACE" in opponent_orders:
            _observer.lost_life -= 1

        if "TORPEDO" in opponent_orders:
            _observer.nb_observer_check += 1
            if MY_LOST_LIFE > 0 :
                game_board[OPP_ID].unknow_opp = False
                game_board[OPP_ID].nearest = True

            text, t1 = opponent_orders.split('|'), ''
            t_list = [ n1 for n1 in text if "TORPEDO" in n1 ]
            t_list = t_list[0].split(' ')

            _,torpedo_opp_x,torpedo_opp_y = t_list[0], int(t_list[1]), int(t_list[2])
            torpedo_opp.torpedo = (torpedo_opp_y, torpedo_opp_x)

            _observer.attach(torpedo_opp)

        if "TRIGGER" in opponent_orders:
            _observer.nb_observer_check += 1
            if MY_LOST_LIFE > 0 :
                game_board[OPP_ID].unknow_opp = False

            text, t1 = opponent_orders.split('|'), ''
            t_list = [ n1 for n1 in text if "TRIGGER" in n1 ]
            t_list = t_list[0].split(' ')

            _,trigger_opp_x,trigger_opp_y = t_list[0], int(t_list[1]), int(t_list[2])
            torpedo_opp.torpedo = (trigger_opp_y, trigger_opp_x)

            _observer.attach(trigger_opp)

        kanban_opp = _observer.update(game_board[OPP_ID],game_board[MY_ID],kanban_opp,kanban_mine)

        _observer.reset()

        for c1, f1, d1 in update_order(opponent_orders):
            if c1 == 'SILENCE':
                TURN_OPP_SILENCE = 0

            if f1 is not None:
                kanban_opp.update(f1,d1)
                kanban_opp = StalkAndTorpedo(kanban_opp)


        TURN_OPP_SILENCE = TURN_OPP_SILENCE + 1 if TURN_OPP_SILENCE != -1 else TURN_OPP_SILENCE

        is_torpedo_attach = False
        if TURN_OPP_SILENCE != 1 :

            g_strategy_state.selection(game_board[OPP_ID], game_board[MY_ID], kanban_opp, kanban_mine, _observer)

            _observer.iterator(game_board[MY_ID],kanban_opp,kanban_mine)

        if game_board[MY_ID].mine == 0 :

            orientation = kanban_mine.mine(game_board[MY_ID])
            if orientation is not None :
                game_board[MY_ID].write_mine(orientation)
                game_board[MY_ID].mine = 3

        if TURN_OPP_SILENCE == 2 and SILENCE_NEED_FUSION == 1 :
            kanban_opp.silence_fusion()
            kanban_opp = StalkAndTorpedo(kanban_opp)

        nearest = game_board[MY_ID].nearest

        if turn <= 15 :
            state = k_STATE_AGENT_STARTING

        elif game_board[MY_ID].unknow_opp == True and game_board[OPP_ID].unknow_opp == True :
            state = k_STATE_AGENT_DISCRETE
            g_strategy_state = StrategyDiscrete(g_strategy_state)

        elif game_board[MY_ID].nearest == True :
            state = k_STATE_AGENT_WARING
            g_strategy_state = StrategyWaring(g_strategy_state)

        elif game_board[MY_ID].unknow_opp == True :
            state = k_STATE_AGENT_SEARCHING
            g_strategy_state = StrategySearching(g_strategy_state)

        elif game_board[OPP_ID].unknow_opp == True :
            state = k_STATE_AGENT_DISCRETE
            g_strategy_state = StrategyDiscrete(g_strategy_state)

        else :
            state = k_STATE_AGENT_MINING
            g_strategy_state = StrategyMining(g_strategy_state)

        print("Kanban Board {} Torpedo {}".format(
        len(kanban_opp.inp),game_board[MY_ID].torpedo),file=sys.stderr)

        print("Mode: {} Opp [{}] Me [{}] Nearest [{}]".format(
            print_agent[state], not game_board[OPP_ID].unknow_opp, not game_board[MY_ID].unknow_opp, nearest),file=sys.stderr)

        text = update_agent(g_strategy_state.agent,game_board[MY_ID])

        y_row, x_col = p1_next.y, p1_next.x
        dir = GET_DIRS[ (y_row - game_board[MY_ID].y, x_col - game_board[MY_ID].x)]
        game_board[MY_ID].write_move(dir,text)

        if game_board[MY_ID].need_surface == True:
            game_board[MY_ID].write_surface()
            game_board[MY_ID].need_surface = False

        turn += 1
        print(game_board[MY_ID].out)
