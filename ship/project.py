from module import Module
from validator import *
from deployer import Deployer
from maven import Maven
from subversion import Subversion

class ProjectBuilder:
    def __init__(self, home, name, config):
        self.home = home
        self.name = name
        self.config = config

        self.source = None
        self.rules = None
        self.builder = None
        self.deploy_params = {}

    def with_subversion(self, url, version):
        self.source = Subversion(url, self.home, self.name, version)
        self.source.checkout()
        return self

    def with_maven(self):
        self._check_source_control()

        self.builder = Maven(self.home + "/" + self.name)
        return self

    def with_tomcat(self, params={}):
        self.deploy_params['tomcat'] = params
        return self

    def with_validation_rules(self, rules):
        self.rules = rules
        return self

    def build(self):
        self.project = Project(self.home, self.name, self.config, self.deploy_params)
        self.project.register_code_build(self.builder)
        self.project.register_validation_rules(self.rules)

        self.project.build()

        return self

    def deploy(self):
        deployer = Deployer(self.project)
        deployer.deploy()        
        return self.project

    def _check_source_control(self):
        if self.source is None:
            raise Exception("You must register a source control system")

class Project:
    def __init__(self, home, name, config, deploy_params):
        self.home = home
        self.name = name
        self.config = config
        self.deploy_params = deploy_params

        self.modules = []
        self.validation_rules = []

    def get_config(self):
        return self.config

    def get_directory(self):
        return self.home + "/" + self.name

    def get_modules(self):
        return self.modules

    def is_multimodule(self):
        return len(self.modules) > 1

    def register_code_build(self, builder):
        self.builder = builder

    def register_validation_rules(self, validation_rules):
        self.validation_rules = validation_rules

    def build(self):
        self.check_dependencies()

        self.builder.build()
        self.validate_quality_rules()

        self.build_module_list()

    def build_module_list(self):
        if self.builder.is_multimodule():
            for module in self.builder.list_modules():
                self.builder.reload(self.home + "/" + self.name + "/" + module)
                self._add_module(self.builder, module)
        else:
            self._add_module(self.builder)

    def validate_quality_rules(self):
        validator = ValidationRuleExecutor(self.validation_rules)
        validator.validate(self)

    def check_dependencies(self):
        self.check_code_build()
        self.check_validation_rules()

    def check_validation_rules(self):
        if self.validation_rules == None:
            raise Exception("You must register a set of build validation rules")

    def check_code_build(self):
        if self.builder == None:
            raise Exception("You must register a code build system")

    def _add_module(self, builder, submodule=None):
        if builder.get_type() == None:
            return

        new_module = Module(self, builder.get_type(), builder.get_packaging(), builder.get_final_name(), submodule)
        self.modules.append(new_module)
