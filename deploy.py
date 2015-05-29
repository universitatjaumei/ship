#!/usr/bin/python2

import argparse
import traceback
from logger import getLogger
from project import Project
from deployer import Deployer
from errors import SVNException, ProjectIdNotFoundException
from structure import DirectoryStructureBuilder
from validator import *
from colors import Colors


class Operation:
    BUILD = "build"
    DEPLOY = "deploy"


class Configuration:
    @staticmethod
    def get_deploy_home():
        return "/opt/devel/workspaces/uji/uji-deployment-tools/deploy/target"


def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="Action to perform with the project", choices=[Operation.BUILD, Operation.DEPLOY])
    parser.add_argument("project", help="3 letters project name");
    parser.add_argument("--environment", choices=['development', 'production'], default="development", help="Environment to deploy")
    parser.add_argument("version", help="Tag  version of the project in subversion");
    parser.add_argument("alternate", help="Optional alternate project ID", nargs="?");

    return parser.parse_args()


def requested_deploy_to_production(args):
    return args.action == Operation.DEPLOY

if __name__ == "__main__":

    args = parse_commandline()
    logger = getLogger("INFO")

    try:
        logger.info(Colors.OKBLUE + "[START] Initializing project construction" + Colors.ENDC)

        executor = ValidationRuleExecutor([ConfigFileValidationRule])
        directory_structure_builder = DirectoryStructureBuilder(Configuration.get_deploy_home())

        project = Project(args.project, args.version, executor, directory_structure_builder)
        project.run()

        if requested_deploy_to_production(args):
            logger.info("[DEPLOY] Deploying to " + args.environment)
            deployer = Deployer(project)
            deployer.run(args.environment)

        logger.info(Colors.OKBLUE + "[END] Finished succesfully!!" + Colors.ENDC)
    except SVNException as e:
        logger.error(Colors.FAIL + "[ERROR] Invalid or unauthorized SVN repository '" + args.project + "'" + Colors.ENDC)

    except ProjectIdNotFoundException as e:
        logger.error(Colors.FAIL + "[ERROR] ProjectID not found in Tomcat" + Colors.ENDC)

    except Exception as e:
        logger.error(e.args[0])
        print traceback.format_exc()
