import sys
import math
import copy
import random
import time

game_board = [ None , None ]
movement_f = { 'N': None,'S': None,'E': None,'W': None }

WIDTH, HEIGHT, MY_ID, OPP_ID = 0 , 0, 0, 0
TREASURE_MAP = []

STARTING_SYMBOLS = 'S'
FINISHING_SYMBOLS = 'F'
OBSTACLE_SYMBOL = 'x'
EMPTY_SYMBOLS = '.'

DIRS = [('N',-1, 0), ('S',1, 0), ('E',0, 1), ('W',0, -1)]
GET_DIRS = { (-1,0) : 'N' , (1,0) : 'S' , (0,1) : 'E' , (0,-1) : 'N' }


def read_map():
    global WIDTH, HEIGHT, MY_ID, OPP_ID
    WIDTH, HEIGHT, MY_ID = [int(i) for i in input().split()]
    OPP_ID = (MY_ID + 1) % 2
    global TREASURE_MAP
    for i in range(HEIGHT):
        TREASURE_MAP.append(list(input()))
        print(TREASURE_MAP[i],file=sys.stderr)

DEEP = 7

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
        dirs = [iter(DIRS)]

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

                elif new_coord in self.finish:
                    path_append(new_coord)
                    dirs_append(iter(DIRS))
                    return path

            else:
                legal_add(path_pop())
                dirs_pop()

class Submarine():

    def __init__(self,clone):
        self.out = ''
        self.x, self.y = 0, 0
        if clone is not None :
            self.treasure_map = copy.deepcopy(clone.treasure_map)
        else :
            self.treasure_map = TREASURE_MAP

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
        self.x , self.y , self.life = 0, 0, 0
        self.torpedo, self.sonar, self.silence, self.mine = 0, 0, 0, 0
        if clone is not None:
            self.turn = clone.turn + 1
            self.x, self.y, self.life = clone.x, clone.y, clone.life
            self.torpedo, self.sonar = clone.torpedo, clone.sonar
            self.silence, self.mine = clone.silence, clone.mine

def update(me,opp):
    me.x, me.y, me.life, opp.life, me.torpedo, me.sonar, me.silence, me.mine = [int(i) for i in input().split()]

if __name__ == '__main__':
    read_map()
    game_board[MY_ID] = Board(game_board[MY_ID])
    game_board[MY_ID].treasure_map = TREASURE_MAP
    puzzle = HamiltonSolver(game_board[MY_ID].treasure_map)
    if puzzle.start == None :
        y_row , x_col = puzzle.coord_random()
        puzzle.start = y_row, x_col
        game_board[MY_ID].treasure_map[x_col][y_row] = ' '
        puzzle.legal.remove( (y_row,x_col) )
        game_board[MY_ID].x, game_board[MY_ID].y = x_col, y_row

    # TODO PRINT
    print("{} {}".format(game_board[MY_ID].x,game_board[MY_ID].y))

    if puzzle.finish == None :
        y_row , x_col = puzzle.coord_random()
        puzzle.finish = y_row, x_col

    solution = puzzle.solve()
    turn = 1

    while True:
        game_board[MY_ID] = Board(game_board[MY_ID])
        game_board[OPP_ID] = Board(game_board[OPP_ID])
        update(game_board[MY_ID],game_board[OPP_ID])

        sonar_result = input()
        print(sonar_result, file=sys.stderr)
        opponent_orders = input()
        print(opponent_orders, file=sys.stderr)

        y_row , x_col = puzzle.read_turn(solution,turn)
        game_board[MY_ID].treasure_map[x_col][y_row] = ' '
        dir = GET_DIRS[ (x_col - game_board[MY_ID].x, y_row - game_board[MY_ID].y)]
        game_board[MY_ID].write_move(dir,'TORPEDO')
        print(game_board[MY_ID].out)

        turn += 1
        #print("MOVE N TORPEDO")
