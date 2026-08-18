import unittest
from scripts.validate_projects import validate

class TestRepositoryStructure(unittest.TestCase):
    def test_projects_follow_contract(self):
        projects,errors=validate()
        self.assertTrue(projects)
        self.assertEqual(errors,[])

if __name__=="__main__": unittest.main()
