import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'assets': [{'name': 'customers', 'columns': ['id', 'email']}, {'name': 'orders', 'columns': ['id', 'amount']}]}
        self.assertEqual(analyze(payload),{'assets': [{'name': 'customers', 'tags': ['contains_pii']}, {'name': 'orders', 'tags': ['internal']}]})
if __name__=="__main__": unittest.main()
