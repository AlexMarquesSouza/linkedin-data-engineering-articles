import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'required': ['owner', 'definition', 'classification'], 'assets': [{'name': 'revenue', 'metadata': {'owner': 'finance', 'definition': 'net revenue', 'classification': 'internal'}}, {'name': 'events', 'metadata': {'owner': 'platform'}}]}
        self.assertEqual(analyze(payload),{'scores': [{'name': 'revenue', 'score': 100.0}, {'name': 'events', 'score': 33.3}]})
if __name__=="__main__": unittest.main()
