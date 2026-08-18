import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'events': [{'capacity': 'c1', 'utilization': 72}, {'capacity': 'c1', 'utilization': 91}, {'capacity': 'c2', 'utilization': 84}], 'threshold': 85}
        self.assertEqual(analyze(payload),{'alerts': [{'capacity': 'c1', 'utilization': 91}]})
if __name__=="__main__": unittest.main()
