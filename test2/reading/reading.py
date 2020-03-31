import sys
sys.path.append('../../')

# Global variables
from test2.test_main import TREASURE_MAP
from test2.test_main import TEXT1
from test2.test_main import TEXT2
from test2.test_main import TEXT3
from test2.test_main import TEXT4
from test2.test_main import TEXT5
from test2.test_main import TEXT6

# Class
from OceanOfCode import StalkAndLegal
from OceanOfCode import StalkAndTorpedo
from OceanOfCode import Submarine
from OceanOfCode import Board

# Global
from OceanOfCode import READ_COMMAND

import unittest

h_command = { ('MOVE')}

class _reading(unittest.TestCase):

    def test_simple(self):

        text1 = TEXT1.split('|')
        print(text1)
        for t in text1:
            print(t)
            if t.find("MOVE") != -1 :
                print("YES")
            else :
                print("NO")

        text1 = TEXT2.split('|')
        print(text1)
        for t in text1:
            print(t)
            if t.find("SILENCE") != -1 :
                print("YES")
            else :
                print("NO")

    def test_use_read_command(self):

        text1 = TEXT1.split('|')
        for t in text1:
            command = next( (c1,f1) for c1,f1 in READ_COMMAND if t.find(c1) != -1 )
            print(command)

        text3 = TEXT3.split('|')
        for t in text3:
            command = next( (c1,f1) for c1,f1 in READ_COMMAND if t.find(c1) != -1 )
            print(command)

        text5 = TEXT5.split('|')
        for t in text5:
            command = next( (c1,f1) for c1,f1 in READ_COMMAND if t.find(c1) != -1 )
            print(command)

    def test_use_read_command2(self):
        text6 = TEXT6.split('|')
        t = ''
        for t in text6:
            command = next( (c1,f1) for c1,f1 in READ_COMMAND if t.find(c1) != -1 )
            print(command)
            data1 = t.split(' ')
            for d1 in data1:
                print(d1)




if __name__ == '__main__':
    unittest.main()
