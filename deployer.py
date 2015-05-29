from __future__ import with_statement
from tomcat import Tomcat
from monit import Monit
from environment import Environment
from commands import set_environment
from validator import ValidationRuleExecutor
from validator import JDBCUrlRemoteCheck


class TomcatDeployer:

    def __init__(self, environment):
        self.environment = environment

    def deploy(self, app, module):
        tomcat = Tomcat(self.environment.get_catalina_home(),
                        self.environment.get_tomcat_username(),
                        self.environment.get_tomcat_password(),
                        self.environment.get_tomcat_hostname(),
                        self.environment.get_tomcat_port(),
                        self.environment.get_tomcat_deploy_directory())

        tomcat.shutdown()
        tomcat.deploy(app, module.get_compiled_filename())
        tomcat.startup()


class MonitDeployer:

    def __init__(self, environment, executor):
        self.environment = environment

    def deploy(self, app, module):
        monit = Monit(self.environment.get_monit_home())
        monit.shutdown_service(app)
        monit.deploy(app, module.get_compiled_filename())
        monit.startup_service(app)


class DeployerFactory:
    _deployers = {
        "webapp": TomcatDeployer,
        "servicio": MonitDeployer
    }

    @staticmethod
    def build(type, environment):
        return DeployerFactory._deployers[type](environment)


class Deployer:

    def __init__(self, project):
        self.project = project
        self.validations = ValidationRuleExecutor([JDBCUrlRemoteCheck])

    def validate(self, environment):
        self.validations.execute(self.project, environment)

    def _deploy(self, module, environment):
        app = self.project.get_project_id()
        deployer = DeployerFactory.build(module.get_type(), environment)
        deployer.deploy(app, module)

    def run(self, environment):
        deploy_environment = Environment(environment, self.project.get_project_id())
        set_environment(deploy_environment)

        self.validate(deploy_environment)
        for module in self.project.get_modules():
            self._deploy(module, deploy_environment)
