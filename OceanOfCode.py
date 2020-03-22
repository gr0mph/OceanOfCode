import sys
import math
import copy

game_board = [ None , None ]
_board = None
movement_f = { 'N': None,'S': None,'E': None,'W': None }

WIDTH, HEIGHT, MY_ID = [int(i) for i in input().split()]
OPP_ID = (MY_ID + 1) % 2
TREASURE_MAP = []
for i in range(HEIGHT):
    TREASURE_MAP.append(input())
    print(TREASURE_MAP[i],file=sys.stderr)

DEEP = 3

#print("7 7")
def select(n):
    row, col = ((n - 1) // 3) * 5 , ((n - 1) % 3) * 5
    SECTOR_MAP = []
    for r1 in range(0,5):
        l_map = list(TREASURE_MAP[row+r1])
        l_map = l_map[ col : col+5]
        SECTOR_MAP.append(''.join(l_map))
    return row, col, SECTOR_MAP

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
        self.legal = set()
        for r, row in enumerate(grid):
            for c, item in enumerate(row):
                if item in STARTING_POINT_SYMBOLS:
                    self.start = (r, c)
                elif item in EMPTY_SPACE_SYMBOLS:
                    self.legal.add((r, c))

    def read_turn(self,path,turn):
        return path[turn]

    def format_solution(self, path):
        """Format a path as a string."""
        grid = [[OBSTACLE_SYMBOL] * self.w for _ in range(self.h)]
        for i, (o,r, c) in enumerate(path, start=1):
            #print('({},{})'.format(r,c))
            grid[r][c] = i
        w = len(str(len(path) + 1)) + 1

        return '\n'.join(''.join(str(item).ljust(w) for item in row)
                         for row in grid)

    def solve(self):
        """Generate solutions as lists of coordinates."""
        r , c = self.start
        result = [ ('S',r, c)]
        path = [self.start]
        dirs = [iter(DIRS)]

        # Cache attribute lookups in local variables
        result_append = result.append
        result_pop = result.pop
        path_append = path.append
        path_pop = path.pop
        legal = self.legal
        legal_add = legal.add
        legal_remove = legal.remove
        dirs_append = dirs.append
        dirs_pop = dirs.pop

        while result:
            #r, c = path[-1]
            o, r, c = result[-1]
            for orientation, dr, dc in dirs[-1]:
                new_coord = r + dr, c + dc
                new_path = orientation, r + dr, c + dc
                if new_coord in legal:
                    result_append(new_path)
                    path_append(new_coord)
                    legal_remove(new_coord)
                    dirs_append(iter(DIRS))
                    if not legal:
                        yield result
                    break
            else:
                result_pop()
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
        self.x , self.y , self.life , self.torpedo, self.sonar, self.silence, self.mine = 0, 0, 0, 0, 0, 0, 0
        if clone is not None:
            self.x, self.y, self.life = clone.x, clone.y, clone.life
            self.torpedo, self.sonar = clone.torpedo, clone.sonar
            self.silence, self.mine = clone.silence, clone.mine

def update(me,opp):
    me.x, me.y, me.life, opp.life, me.torpedo, me.sonar, me.silence, me.mine = [int(i) for i in input().split()]

_board = Board

# TODO...
SECTOR_MAP = select(4)
r1 = 5
for r in SECTOR_MAP:
    c1 = 0
    for c in r:
        if c != 'x':
            break
    l_r = list(r)
    l_r[c1] ='S'
    r = ''.join(l_r)


puzzle = HamiltonSolver(SECTOR_MAP)

while True:
    game_board[MY_ID] = _board(game_board[MY_ID])
    game_board[OPP_ID] = _board(game_board[OPP_ID])
    update(game_board[MY_ID],game_board[OPP_ID])

    sonar_result = input()
    print(sonar_result, file=sys.stderr)
    opponent_orders = input()
    print(opponent_orders, file=sys.stderr)

    print("MOVE N TORPEDO")
