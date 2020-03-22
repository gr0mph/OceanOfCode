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

if __name__ == '__main__':
    unittest.main()
