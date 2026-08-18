import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'activities': [{'id': 'a', 'updated': 1}, {'id': 'b', 'updated': 1}, {'id': 'a', 'updated': 3}]}
        self.assertEqual(analyze(payload),{'latest': [{'id': 'a', 'updated': 3}, {'id': 'b', 'updated': 1}]})
if __name__=="__main__": unittest.main()
