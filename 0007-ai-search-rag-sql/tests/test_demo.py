import unittest
from src.demo import analyze
class TestDemo(unittest.TestCase):
    def test_expected_scenario(self):
        payload={'query': 'governanca dados', 'documents': [{'id': 'd1', 'text': 'governanca e catalogo de dados'}, {'id': 'd2', 'text': 'otimizacao de clusters spark'}, {'id': 'd3', 'text': 'qualidade e governanca'}]}
        self.assertEqual(analyze(payload),{'ranking': ['d1', 'd3']})
if __name__=="__main__": unittest.main()
