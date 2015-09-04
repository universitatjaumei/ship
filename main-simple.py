#!/usr/bin/python2

import traceback

from ship.logger import ShipLogger
from ship.project import ProjectBuilder
from ship.validator import *
from ship.errors import SVNException, ProjectIdNotFoundException

ENVIRONMENT = "sample"
HOME = "/tmp/target"
URL = "svn://localhost/repos/SAMPLE"
PROJECT_NAME = "sample"
KEY = "smp"
VERSION = "trunk"

if __name__ == "__main__":
    logger = ShipLogger("INFO")

    try:
        logger.success("Initializing project construction")

        rules = [ ConfigFileValidationRule, ConsoleLogValidationRule,
                  PomXMLValidationRule, CompiledPackageExistsValidationRule ]

        project = ProjectBuilder(HOME, PROJECT_NAME, "/etc/uji/%s/app.properties" % KEY) \
            .with_subversion(URL, VERSION) \
            .with_maven() \
            .with_validation_rules(rules) \
            .build() \
            .deploy(ENVIRONMENT)

        logger.success("Finished succesfully!!")
    except SVNException as e:
        logger.error("Invalid or unauthorized SVN repository '" + PROJECT_NAME + "'")

    except ProjectIdNotFoundException as e:
        logger.error("ProjectID not found in Tomcat")

    except Exception as e:
        print traceback.format_exc()
