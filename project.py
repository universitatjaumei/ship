from module import Module
from validator import *
from deployer import Deployer

class Project:
    def __init__(self, home, name, config, source):
        self.check_source_control(source)

        self.home = home
        self.name = name
        self.config = config
        self.source = source

        self.modules = []
        self.validation_rules = []

        self.source.checkout()

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
                self.add_module(self.builder, module)
        else:
            self.add_module(self.builder)

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

    def check_source_control(self, source):
        if source == None:
            raise Exception("You must register a source control system")

    def deploy(self, environment):
        deployer = Deployer(self)
        deployer.deploy(environment)

    def add_module(self, builder, submodule=None):
        if builder.get_type() == None:
            return

        new_module = Module(self, builder.get_type(), builder.get_packaging(), builder.get_final_name(), submodule)
        self.modules.append(new_module)