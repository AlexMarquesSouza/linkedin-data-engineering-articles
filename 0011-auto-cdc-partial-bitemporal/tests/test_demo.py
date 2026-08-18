import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'initial': {'id': 1, 'name': 'Ana', 'city': 'SP'}, 'events': [{'sequence': 2, 'changes': {'city': 'BH'}}, {'sequence': 1, 'changes': {'name': 'Ana Silva'}}]}
        self.assertEqual(analyze(payload),{'current': {'id': 1, 'name': 'Ana Silva', 'city': 'BH'}, 'applied_sequence': [1, 2]})
if __name__=="__main__": unittest.main()
