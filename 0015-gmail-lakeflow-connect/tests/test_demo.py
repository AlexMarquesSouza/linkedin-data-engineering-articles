import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'cursor_day': 10, 'messages': [{'id': 'm1', 'day': 9}, {'id': 'm1', 'day': 11}, {'id': 'm2', 'day': 12}, {'id': 'm3', 'day': 3}]}
        self.assertEqual(analyze(payload),{'ingested': ['m1', 'm2'], 'new_cursor_day': 12})
if __name__=="__main__": unittest.main()
