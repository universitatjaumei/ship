class Module:
    def __init__(self, project, type, packaging, final_name, submodule=None):
        self.project = project
        self.type = type
        self.packaging = packaging
        self.final_name = final_name
        self.submodule = submodule

    def get_type(self):
        return self.type

    def get_packaging(self):
        return self.packaging

    def get_name(self):
        return self.final_name

    def get_directory(self):
        dir = self.project.get_directory()

        if self.submodule != None:
           dir = dir + "/" + self.submodule

        return dir