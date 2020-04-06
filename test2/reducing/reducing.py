import sys
sys.path.append('../../')

# Global variables
from test2.test_map import TREASURE_MAP

import unittest

class _reducing(unittest.TestCase):

    def test_global(self):
        for t_r in TREASURE_MAP:
            print(t_r)

if __name__ == '__main__':
    unittest.main()
