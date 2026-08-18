import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'current': '18-LTS', 'target': '19', 'dependencies': [{'name': 'legacy-jdk-lib', 'supports': ['18-LTS']}, {'name': 'arrow-udf', 'supports': ['18-LTS', '19']}]}
        self.assertEqual(analyze(payload),{'ready': False, 'blockers': ['legacy-jdk-lib']})
if __name__=="__main__": unittest.main()
