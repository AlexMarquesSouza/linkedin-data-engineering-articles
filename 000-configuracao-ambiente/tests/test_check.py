import unittest
from src.check import inspect
class TestCheck(unittest.TestCase):
    def test_contract(self): self.assertIn("python3",inspect()["tools"])
if __name__=="__main__": unittest.main()
