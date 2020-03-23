import unittest

TRANSIT_SET = ( None, ('1S','1E') , ('2W','2S','2E') , ('3W','3S') ,
                ('4N', '4E', '4S') , ('5N' , '5E' , '5S' , '5W') , ('6N','6W','6S') ,
                ('7N' , '7E') , ('8W', '8N', '8E') , ('9W','9N') )

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

#for h in TREASURE_MAP:
#    print(h)

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
    TRANSIT_SECTOR = {}
    for i in range(1,10):
        TRANSIT_SECTOR[str(i)+'S'] = set()
        TRANSIT_SECTOR[str(i)+'N'] = set()
        TRANSIT_SECTOR[str(i)+'W'] = set()
        TRANSIT_SECTOR[str(i)+'E'] = set()

    ROW_HEIGHT = ( (4,5) , (9,10) )
    for r1, r2 in ROW_HEIGHT:
        for c1 in range (0,15):
            if TREASURE_MAP[r1][c1] == '.' and TREASURE_MAP[r2][c1] == '.' :
                TRANSIT_SECTOR[str(sector(c1,r1))+'S'].add((c1,r1))
                TRANSIT_SECTOR[str(sector(c1,r2))+'N'].add((c1,r2))

    COL_WIDTH = ( (4,5) , (9,10) )
    for r1 in range(0,15):
        for c1, c2 in COL_WIDTH:
            if TREASURE_MAP[r1][c1] == '.' and TREASURE_MAP[r1][c2] == '.':
                TRANSIT_SECTOR[str(sector(c1,r1))+'E'].add((c1,r1))
                TRANSIT_SECTOR[str(sector(c2,r1))+'W'].add((c2,r1))

    return TRANSIT_SECTOR


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
        TRANSIT_SECTOR = prepare(TREASURE_MAP)
        for i in range(1,10):
            print('SECTOR {}'.format(i))
            for t_s in TRANSIT_SET[i] :
                print(t_s)
                for r1,c1 in TRANSIT_SECTOR[t_s]:
                    print('Sector : {} ({},{})'.format(sector(r1,c1),r1,c1))



if __name__ == '__main__':
    unittest.main()
