import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'files': [{'id': 'a', 'version': 1}, {'id': 'a', 'version': 2}, {'id': 'b', 'version': 1}]}
        self.assertEqual(analyze(payload),{'latest': [{'id': 'a', 'version': 2}, {'id': 'b', 'version': 1}]})
if __name__=="__main__": unittest.main()
