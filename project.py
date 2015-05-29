from validator import ValidationRuleExecutor
from validator import PomXMLValidationRule
from validator import CompiledPackageExistsValidationRule
from validator import WebXmlValidationRule
from validator import ConsoleLogValidationRule
from module import Module
from maven import Maven
from subversion import Subversion
from logger import getLogger


class Project:
    def __init__(self, project, version, executor, directory_structure_builder):
        self.project_id = project.lower()
        self.project_name = Subversion.get_project_name(self.project_id)
        self.version = version.lower()
        self.executor = executor
        self.logger = getLogger()
        self.maven = None

        self._create_directory_structure(directory_structure_builder)
        self._checkout_project_code()
        self._modules = []

    def _create_directory_structure(self, directory_structure_builder):
        self.directory_structure_builder = directory_structure_builder
        self.directory_structure_builder.build(self.project_id)

    def _checkout_project_code(self):
        self.subversion = Subversion(self.get_homedir(), self.project_id)
        self.subversion.checkout(self.version)

    def get_project_id(self):
        return self.project_id

    def build(self):
        self.logger.info('[BUILD] Building project')

        self.maven = Maven(self.get_homedir())
        self.maven.build()

        module_executor = ValidationRuleExecutor([ConsoleLogValidationRule,
                                                  PomXMLValidationRule,
                                                  CompiledPackageExistsValidationRule,
                                                  WebXmlValidationRule])

        if self.maven.is_multimodule():
            for module_name in self.maven.list_modules():
                module_maven = Maven(self.get_homedir() + "/" + module_name)
                module = Module(module_executor, self, module_maven, module_name)
                module.validate()
                self._modules.append(module)
        else:
            module = Module(module_executor, self, self.maven)
            module.validate()
            self._modules.append(module)

    def get_modules(self):
        return self._modules

    def get_homedir(self):
        return "%s/%s/%s" % (self.directory_structure_builder.get_deploy_home(),
                             self.project_id.upper(),
                             self.project_name)

    def get_app_properties(self):
        return "/etc/uji/%s/app.properties" % self.project_id

    def run(self):
        self.executor.execute(self, None)
        self.build()
