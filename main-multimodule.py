#!/usr/bin/python2

import traceback

from logger import ShipLogger

from project import Project
from validator import *
from subversion import Subversion
from errors import SVNException, ProjectIdNotFoundException
from maven import Maven

ENVIRONMENT = "production"
HOME = "/tmp/target"
URL = "svn://localhost/repos/SAMPLE-MULTIMODULE"
PROJECT_NAME = "sample-multimodule"
KEY = "smp"
VERSION = "trunk"

if __name__ == "__main__":
    logger = ShipLogger("INFO")

    try:
        logger.success("Initializing project construction")

        source = Subversion(URL, HOME, PROJECT_NAME, VERSION)

        project = Project(HOME, PROJECT_NAME, "/etc/uji/%s/app.properties" % KEY, source)

        builder = Maven(HOME + "/" + PROJECT_NAME)
        project.register_code_build(builder)

        project.register_validation_rules([
            ConfigFileValidationRule,
            ConsoleLogValidationRule,
            PomXMLValidationRule,
            CompiledPackageExistsValidationRule
        ])

        project.build()
        project.deploy(ENVIRONMENT)

        logger.success("Finished succesfully!!")
    except SVNException as e:
        logger.error("Invalid or unauthorized SVN repository '" + PROJECT_NAME + "'")

    except ProjectIdNotFoundException as e:
        logger.error("ProjectID not found in Tomcat")

    except Exception as e:
        print traceback.format_exc()
