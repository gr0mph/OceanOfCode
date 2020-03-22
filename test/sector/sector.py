import unittest


TREASURE_MAP = []
TREASURE_MAP.append('.xx.....xx.....')
TREASURE_MAP.append('........xx.....')
TREASURE_MAP.append('.xx............')
TREASURE_MAP.append('.xx............')
TREASURE_MAP.append('....xx.........')
TREASURE_MAP.append('....xx.....xx..')
TREASURE_MAP.append('...........xx..')
TREASURE_MAP.append('...............')
TREASURE_MAP.append('..........xx...')
TREASURE_MAP.append('..........xx.xx')
TREASURE_MAP.append('..........xx.xx')
TREASURE_MAP.append('.....xx........')
TREASURE_MAP.append('.....xx........')
TREASURE_MAP.append('.....xx........')
TREASURE_MAP.append('.....xx........')


H_SECTOR1 = {
    (4,0) : None if TREASURE_MAP[0][4] == 'x' else True
}


for h in TREASURE_MAP:
    print(h)

def sector(x,y):
    s = (x // 5) + 1 + ( (y // 5) * 3 )
    return s

def select(n,TREASURE_MAP):
    row, col = ((n - 1) // 3) * 5 , ((n - 1) % 3) * 5
    SECTOR_MAP = []
    for r1 in range(0,5):
        l_map = list(TREASURE_MAP[row+r1])
        l_map = l_map[ col : col+5]
        SECTOR_MAP.append(''.join(l_map))
    return row, col, SECTOR_MAP

def prepare(TREASURE_MAP):
    TRANSIT_SECTOR = []
    TRANSIT_SECTOR.append(None)
    for i in range(1,10):
        TRANSIT_SECTOR.append(set())

    ROW_HEIGHT = (4,5,9,10)
    for r1 in ROW_HEIGHT:
        for c1 in range (0,15):
            if TREASURE_MAP[r1][c1] == '.':
                TRANSIT_SECTOR[sector(r1,c1)].add((r1,c1))

    COL_WIDTH = (4,5,9,10)
    for r1 in range(0,15):
        for c1 in COL_WIDTH:
            if TREASURE_MAP[r1][c1] == '.':
                TRANSIT_SECTOR[sector(r1,c1)].add((r1,c1))

    nb = 1
    for t in TRANSIT_SECTOR:
        if t is None :
            continue
        print()
        r, c, SELECT_MAP = select(nb,TREASURE_MAP)
        for line in SELECT_MAP:
            print(line)

        for s in t:
            print(s)
        nb += 1


class _sector(unittest.TestCase):

    def test_sector(self):
        print()
        for x in range(0,15):
            for y in  range(0,15):
                s = sector(x,y)
                #print('x {} y {} s {} '.format(x,y,s))

        # Example
        s = sector(3,9)
        print('x {} y {} s {} '.format(3,9,s))


    def test_select(self):
        print()
        for n in range(1,10):
            r, c, SELECT_MAP = select(n,TREASURE_MAP)
            #print('n {} r {} c {}'.format(n,r,c))
            #for line in SELECT_MAP:
            #   print(line)

        # Example
        r, c, SELECT_MAP = select(5,TREASURE_MAP)
        for line in SELECT_MAP:
            print(line)

    def test_prepare(self):
        print()
        prepare(TREASURE_MAP)

if __name__ == '__main__':
    unittest.main()
