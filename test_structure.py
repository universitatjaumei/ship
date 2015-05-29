import os, shutil, unittest

from structure import DirectoryStructureBuilder

DEPLOY_HOME = "/tmp"
PROJECT = "UPO"

PROJECT_HOME = "%s/%s" % (DEPLOY_HOME, PROJECT)

def create_an_existing_structure():
    if os.path.isdir(PROJECT_HOME):
        shutil.rmtree(PROJECT_HOME)

    os.makedirs(PROJECT_HOME)

def create_a_dummy_file_on_existing_structure():
    open("%s/fichero.txt" % PROJECT_HOME, "w").write("TEST")

def dummy_file_doesnt_exist():
    return not os.path.isfile("%s/fichero.txt" % PROJECT_HOME)

def clear_project_directory():
    if os.path.isdir(PROJECT_HOME):
        shutil.rmtree(PROJECT_HOME)

class TestDirectoryStructureBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = DirectoryStructureBuilder(DEPLOY_HOME)

    def test_structure_should_be_build_when_not_exists(self):
        self.builder.build(PROJECT)

        self.assertTrue(os.path.isdir(PROJECT_HOME))

    def test_structure_should_be_recreate_when_exists(self):
        create_an_existing_structure()
        create_a_dummy_file_on_existing_structure()

        self.builder.build(PROJECT)

        self.assertTrue(dummy_file_doesnt_exist())

    def tearDown(self):
        clear_project_directory()

if __name__ == '__main__':
    unittest.main()
