from __future__ import with_statement
from tomcat import Tomcat
from monit import Monit
from environment import Environment
from commands import set_environment
from validator import ValidationRuleExecutor
from validator import JDBCUrlRemoteCheck

class TomcatDeployer:
    def __init__(self, environment, params):
        self.environment = environment

        if 'tomcat' in params:
            self.params = params['tomcat']
        else:
            self.params = {}

    def deploy(self, module):
        tomcat = Tomcat(self.environment)

        tomcat.deploy(module)
        tomcat.shutdown()

        if not 'start_tomcat_after_deploy' in self.params or self.params['start_tomcat_after_deploy']:
            tomcat.startup()

class MonitDeployer:
    def __init__(self, environment, executor, params):
        self.environment = environment

        if 'monit' in params:
            self.params = params['monit']
        else:
            self.params = {}

    def deploy(self, module):
        app = module.get_name()

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
    def build(type, environment, params):
        return DeployerFactory._deployers[type](environment, params)


class Deployer:
    def __init__(self, project):
        self.project = project
        self.deploy_params = self.project.deploy_params
        #self.validations = ValidationRuleExecutor([JDBCUrlRemoteCheck])

    def validate(self, environment):
        self.validations.execute(self.project, environment)

    def _deploy(self, module, environment, params):
        deployer = DeployerFactory.build(module.get_type(), environment, params)
        deployer.deploy(module)

    def deploy(self, environment):
        #self.validate(deploy_environment)

        for module in self.project.get_modules():
            deploy_environment = Environment(module.get_name())
            set_environment(deploy_environment)
            self._deploy(module, deploy_environment, self.deploy_params)
