import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'allowed': ['drive.read', 'github.read'], 'requests': ['drive.read', 'slack.write', 'github.read']}
        self.assertEqual(analyze(payload),{'allowed': ['drive.read', 'github.read'], 'blocked': ['slack.write']})
if __name__=="__main__": unittest.main()
