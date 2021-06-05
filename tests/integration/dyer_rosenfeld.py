import unittest

class dyer_rosenfeld(unittest.TestCase):
    def setUp(self):
        self.trueValue = True

    def test_always_passes(self):
        self.assertTrue(self.trueValue)

if __name__ == '__main__':
    unittest.main()

