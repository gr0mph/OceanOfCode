import unittest

def sector(x,y):
    s = (x // 5) + 1 + ( (y // 5) * 3 )
    return s

class _sector(unittest.TestCase):

    def test_sector(self):
        for x in range(0,15):
            for y in  range(0,15):
                s = sector(x,y)
                print('x {} y {} s {} '.format(x,y,s))

if __name__ == '__main__':
    unittest.main()
