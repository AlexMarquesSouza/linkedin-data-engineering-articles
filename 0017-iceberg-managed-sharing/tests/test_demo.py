import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'required': ['iceberg-rest', 'v2', 'read'], 'clients': [{'name': 'engine-a', 'features': ['iceberg-rest', 'v2', 'read']}, {'name': 'engine-b', 'features': ['iceberg-rest', 'v1', 'read']}]}
        self.assertEqual(analyze(payload),{'compatible': ['engine-a'], 'incompatible': ['engine-b']})
if __name__=="__main__": unittest.main()
