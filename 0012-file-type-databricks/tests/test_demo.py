import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'files': [{'name': 'invoice.pdf', 'mode': 'MANAGED', 'uri': '/Volumes/docs/invoice.pdf'}, {'name': 'photo.jpg', 'mode': 'EXTERNAL', 'uri': 'abfss://media/photo.jpg'}, {'name': 'bad.txt', 'mode': 'UNKNOWN', 'uri': '/tmp/bad'}]}
        self.assertEqual(analyze(payload),{'valid': ['invoice.pdf', 'photo.jpg'], 'invalid': ['bad.txt']})
if __name__=="__main__": unittest.main()
