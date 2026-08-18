import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'usage': [{'cost': 12.5, 'tags': {'team': 'sales'}}, {'cost': 7.5, 'tags': {}}, {'cost': 5.0, 'tags': {'team': 'sales'}}]}
        self.assertEqual(analyze(payload),{'total_cost': 25.0, 'allocated_cost': 17.5, 'unallocated_cost': 7.5, 'coverage_percent': 70.0})
if __name__=="__main__": unittest.main()
