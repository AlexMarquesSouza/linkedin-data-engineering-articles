import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'records': [{'id': 1, 'payload': {'country': 'BR', 'device': 'mobile'}}, {'id': 2, 'payload': {'country': 'BR', 'device': 'web'}}], 'fields': ['country', 'device']}
        self.assertEqual(analyze(payload),{'columns': {'country': ['BR', 'BR'], 'device': ['mobile', 'web']}})
if __name__=="__main__": unittest.main()
