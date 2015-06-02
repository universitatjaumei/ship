from xml.dom import minidom
from commands import *

class Maven:
    def __init__(self, project_directory):
        self.reload(project_directory)

    def reload(self, project_directory):
        self.project_directory = project_directory
        self.pomxml = minidom.parse(self.get_pomxml())

    def get_pomxml(self):
        return "%s/pom.xml" % self.project_directory

    def get_pomxml_modules_node(self):
        modules = self.pomxml.getElementsByTagName("modules")

        if len(modules) == 0:
            return None

        return modules[0]

    def get_final_name(self):
        finalName = self.pomxml.getElementsByTagName("finalName")
        if finalName is not None and len(finalName) > 0:
            return finalName[0].childNodes[0].nodeValue

    def get_type(self):
        itemlist = self.pomxml.getElementsByTagName("packaging")

        project_type = None

        if len(itemlist) == 1 and itemlist[0].childNodes[0].nodeValue == "war":
            project_type = "webapp"
        else:
            itemlist = self.pomxml.getElementsByTagName("uji.tipo")
            if len(itemlist) == 1 and itemlist[0].childNodes[0].nodeValue:
                project_type = itemlist[0].childNodes[0].nodeValue

        return project_type

    def get_packaging(self):
        packaging = self.pomxml.getElementsByTagName("packaging") 
        if packaging is not None and len(packaging) > 0:
           return packaging[0].childNodes[0].nodeValue 

    def is_multimodule(self):
        return self.get_pomxml_modules_node() != None

    def list_modules(self):
        if not self.is_multimodule():
            return []

        modules_node = self.get_pomxml_modules_node()
        return [m.firstChild.nodeValue for m in modules_node.childNodes if m.firstChild is not None]

    def get_project_directory(self):
        return self.project_directory

    def build(self):
        local("cd %s; mvn -DskipTests clean install" % self.project_directory)

if __name__ == "__main__":
    maven = Maven("target/ADE/uji-ade/uji-ade-bd2storage")
    print maven.is_multimodule()
    print maven.list_modules()
    print maven.get_final_name()
