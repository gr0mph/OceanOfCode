import sys
import math
import copy
import random
import time
import gc

AGENT_TORPEDO = 0   # 3,2,1,0
#AGENT_SONAR = 1
AGENT_SILENCE = 1
AGENT_MINE = 2

game_board = [ None , None ]
movement_f = { 'N': None,'S': None,'E': None,'W': None }
select_a = [ 'TORPEDO' , 'SILENCE' , 'MINE' ]

WIDTH, HEIGHT, MY_ID, OPP_ID = 0 , 0, 0, 0
TREASURE_MAP = []

STARTING_SYMBOLS = 'S'
FINISHING_SYMBOLS = 'F'
OBSTACLE_SYMBOL = 'x'
EMPTY_SYMBOLS = '.'

DIRS = [('N',-1, 0), ('S',1, 0), ('E',0, 1), ('W',0, -1)]
GET_DIRS = { (-1,0) : 'N' , (1,0) : 'S' , (0,1) : 'E' , (0,-1) : 'W' }

OPPONENT_SET = set()

def read_map():
    global WIDTH, HEIGHT, MY_ID, OPP_ID
    WIDTH, HEIGHT, MY_ID = [int(i) for i in input().split()]
    OPP_ID = (MY_ID + 1) % 2
    global TREASURE_MAP
    for i in range(HEIGHT):
        TREASURE_MAP.append(list(input()))
        #print(TREASURE_MAP[i],file=sys.stderr)

def t_check_map(TREASURE_MAP):
    for i in range(HEIGHT):
        print(TREASURE_MAP[i],file=sys.stderr)

DEEP = 10

class HamiltonSolver:
    """Solver for a Hamilton Path problem."""

    def __init__(self, grid):
        """Initialize the HamiltonSolver instance from a grid, which must be a
        list of strings, one for each row of the grid.
        """
        self.grid = grid
        self.h = h = len(grid)
        self.w = w = len(grid[0])
        self.start = None
        self.finish = None
        self.legal = set()
        for r, row in enumerate(grid):
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
        self.out = set()
        self.inp = set()
        self.legal = set()
        if clone is not None :
            self.inp = clone.out
            self.legal = clone.legal
            self.treasure_map = clone.treasure_map

    def set_up(self,TREASURE_MAP):
        self.treasure_map = TREASURE_MAP
        for y_row, row in enumerate(self.treasure_map):
            for x_col, item in enumerate(row):
                if item in EMPTY_SYMBOLS:
                    self.legal.add( (y_row, x_col) )

    def mine(self,board):
        mine = Point(None)
        dirs = [iter(DIRS)]
        orientation, y_drow, x_dcol = '', 0, 0
        for orientation, y_drow, x_dcol in dirs[-1]:
            new_coord = board.y + y_drow, board.x + x_dcol
            if new_coord in self.legal:
                self.legal.remove(new_coord)
                break

        if orientation == '' :
            return None

        mine.y, mine.x = board.y + y_drow, board.x + x_dcol
        self.out.add(mine)
        return orientation

    def trigger(self,mine):
        new_coord = mine.y, mine.x
        self.legal.add(new_coord)
        self.out.remove(mine)

    def nearby(self,board):
        for coord in self.inp:
            y_row, x_col = coord
            mine = Point(x_col,y_row)
            if square(mine,board) == True:
                return mine
        return None

    def __iter__(self):
        for m1 in self.inp:
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
        if len(self.inp) >= 10:
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


class Point():

    def __init__(self,x,y):
        self.x, self.y = x, y

class Mine(Point):

    def __init__(self,x,y):
        super().__init__(x,y)
        self.nb = 0

class Submarine():

    def __init__(self,clone):
        self.out = ''
        if clone is not None :
            self.x, self.y = clone.x, clone.y
            self.treasure_map = copy.deepcopy(clone.treasure_map)
        else :
            self.x, self.y = 0, 0
            self.treasure_map = copy.deepcopy(TREASURE_MAP)

    @property
    def sector(self):
        return 1 + (self.x // 5) + ( (self.y // 5) * 3 )

    # MOVE DIRECTION {NORTH, EAST, WEST, SOUTH} LOAD {TORPEDO,SONAR,etc}
    def write_move(self,direction,load):
        t = f'MOVE {direction} {load}'
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


def manhattan(obj1,obj2):
    distance = abs(obj1.x - obj2.x) + abs(obj1.y - obj2.y)
    return distance

def square(obj1,obj2):
    is_true = True
    is_true &= False if abs(obj1.x - obj2.x) > 1 else True
    is_true &= False if abs(obj1.y - obj2.y) > 1 else True
    return is_true

def path_solving(game_board,puzzle):
    game_board[MY_ID].treasure_map[game_board[MY_ID].y][game_board[MY_ID].x] = 'D'
    puzzle.start = game_board[MY_ID].y , game_board[MY_ID].x

    # TODO: Idea but not finished or not done good result
    if puzzle.finish == None :
        y_row , x_col = puzzle.coord_random()
        puzzle.finish = y_row, x_col

    solution = puzzle.solve()
    return game_board, puzzle, solution

if __name__ == '__main__':
    read_map()
    game_board[MY_ID] = Board(game_board[MY_ID])
    puzzle = HamiltonSolver(game_board[MY_ID].treasure_map)
    y_row , x_col = puzzle.coord_random()
    puzzle.legal.remove( (y_row,x_col) )
    game_board[MY_ID].x, game_board[MY_ID].y = x_col, y_row
    game_board, puzzle, solution = path_solving(game_board,puzzle)

    kanban_opp = StalkAndTorpedo(None)
    kanban_opp.set_up(TREASURE_MAP)


    print("{} {}".format(game_board[MY_ID].x,game_board[MY_ID].y))

    turn = 1

    while True:
        print('TURN {}'.format(turn),file=sys.stderr)
        game_board[MY_ID] = Board(game_board[MY_ID])
        game_board[OPP_ID] = Board(game_board[OPP_ID])
        update(game_board[MY_ID],game_board[OPP_ID])

        if turn == DEEP + 1 :
            puzzle = HamiltonSolver(game_board[MY_ID].treasure_map)
            game_board, puzzle, solution = path_solving(game_board,puzzle)

            if solution is None :
                # TODO: WARNING : Write a state in this case

                game_board[MY_ID].treasure_map = TREASURE_MAP
                game_board[MY_ID].write_surface()
                game_board[MY_ID].treasure_map[game_board[MY_ID].y][game_board[MY_ID].x] = 'D'

            elif len(solution) != (DEEP + 1) :
                # TODO: WARNING : Write a state in this case

                game_board[MY_ID].treasure_map = TREASURE_MAP
                game_board[MY_ID].write_surface()
                game_board[MY_ID].treasure_map[game_board[MY_ID].y][game_board[MY_ID].x] = 'D'

            else :
                turn = 1

        #t_check_map(game_board[MY_ID].treasure_map)

        sonar_result = input()
        print(sonar_result, file=sys.stderr)
        opponent_orders = input()
        if opponent_orders is None:
            print("What the fuck ?", file=sys.stderr)
        for c1, f1, d1 in update_order(opponent_orders):
            if f1 is not None:
                kanban_opp.update(f1,d1)
                kanban_opp = StalkAndTorpedo(kanban_opp)

        print("Len Kanban Board {} Torpedo {}".format(len(kanban_opp.inp),game_board[MY_ID].torpedo),file=sys.stderr)
        #if len(kanban_opp.inp) <= 10 :
        #    for b1,s1 in kanban_opp.inp:
        #        print("submarin x {} y {}".format(b1.x,b1.y),file=sys.stderr)

        if game_board[MY_ID].mine == 0 :
            pass

        if game_board[MY_ID].torpedo == 0 and len(kanban_opp.inp) <= 20 :

            print("Search for torpedo",file=sys.stderr)

            for s1,_ in kanban_opp.inp :
                distance = manhattan(s1,game_board[MY_ID])
                if  distance >= 2 and distance <= 4 :
                    game_board[MY_ID].write_torpedo(s1.x,s1.y)
                    game_board[MY_ID].torpedo = 3
                    break


        #d, dy_row, dx_col = next( result_dir for result_dir in DIRS if data in result_dir )
        info = update_agent(game_board[MY_ID])
        text = ''
        try :
            i1 = next(i1 for i1,agent1 in enumerate(info) if agent1 != 0)
            text = select_a[i1]
        except StopIteration:
            text = 'SONAR'

        if turn > 0 and turn < DEEP + 1 :
            y_row , x_col = puzzle.read_turn(solution,turn)
            game_board[MY_ID].treasure_map[y_row][x_col] = 'D'
            dir = GET_DIRS[ (y_row - game_board[MY_ID].y, x_col - game_board[MY_ID].x)]
            #game_board[MY_ID].write_move(dir,'TORPEDO')
            game_board[MY_ID].write_move(dir,text)
            turn += 1

        print(game_board[MY_ID].out)

        #print("MOVE N TORPEDO")
