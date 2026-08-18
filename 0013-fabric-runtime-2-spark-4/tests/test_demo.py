import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'target_python': '3.11', 'libraries': [{'name': 'pandas', 'python': ['3.10', '3.11']}, {'name': 'legacy-wheel', 'python': ['3.10']}]}
        self.assertEqual(analyze(payload),{'compatible': ['pandas'], 'incompatible': ['legacy-wheel']})
if __name__=="__main__": unittest.main()
