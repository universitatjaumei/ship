import logging


class Module:
    def __init__(self, executor, project, maven, submodule_name=None):
        self.executor = executor
        self.project = project
        self.maven = maven
        self.submodule_name = submodule_name

    def get_type(self):
        return self.maven.get_type()

    def get_final_name(self):
        return self.maven.get_final_name()

    def __str__(self):
        return self.submodule_name

    def get_compiled_filename(self):
        if self.get_type() == 'webapp':
            return '%s/target/%s.war' % (self.get_directory(),
                                         self.get_final_name())
        elif self.get_type() == 'servicio':
            return '%s/target/%s.jar' % (self.get_directory(),
                                         self.get_final_name())

    def get_directory(self):
        if self.submodule_name is not None:
            return "%s/%s" % (self.project.get_homedir(), self.submodule_name)
        else:
            return self.project.get_homedir()

    def validate(self):
        if self.submodule_name is not None:
            logging.info("[VALIDATE] Module %s:%s" % (self.project.project_name,
                                                      self.submodule_name))
        else:
            logging.info("[VALIDATE] Module %s" % self.project.project_name)

        self.executor.execute(self.project, self)
