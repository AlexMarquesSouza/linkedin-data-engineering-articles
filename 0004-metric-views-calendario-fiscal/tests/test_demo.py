import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'periods': [{'index': 1, 'value': 100}, {'index': 2, 'value': 120}, {'index': 3, 'value': 80}]}
        self.assertEqual(analyze(payload),{'trailing_2': [{'index': 1, 'average': 100.0}, {'index': 2, 'average': 110.0}, {'index': 3, 'average': 100.0}]})
if __name__=="__main__": unittest.main()
