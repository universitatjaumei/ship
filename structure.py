import os
import shutil
import logging


class DirectoryStructureBuilder:
    def __init__(self, deploy_home):
        self.deploy_home = deploy_home

    def get_deploy_home(self):
        return self.deploy_home

    def build(self, project_name):
        logging.debug('[STRUCTURE] Creating the build directories and cleaning old compilations')

        home_dir = "%s/%s" % (self.deploy_home, project_name.upper())

        if not os.path.isdir(self.deploy_home):
            os.makedirs(self.deploy_home)

        if os.path.isdir(home_dir):
            shutil.rmtree(home_dir)

        os.makedirs(home_dir)
