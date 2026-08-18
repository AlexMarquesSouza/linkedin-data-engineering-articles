import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'operations': ['filter', 'python_udf', 'unsupported_custom_op', 'scala_udf'], 'native_supported': ['filter', 'python_udf', 'scala_udf']}
        self.assertEqual(analyze(payload),{'native': 3, 'fallback': 1, 'fallback_operations': ['unsupported_custom_op']})
if __name__=="__main__": unittest.main()
