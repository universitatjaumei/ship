import yaml
from errors import ProjectIdNotFoundException


class Environment:

    def __init__(self, environment, project_id):
        f = open('environment.yml')
        data = yaml.safe_load(f)
        f.close()
        self.id = environment
        self.data = data[environment]
        self.project_id = project_id

    def get_environment_id(self):
        return self.id

    def get_username(self):
        return self.data["username"]

    def get_hostname(self):
        return self.data["hostname"]

    def get_host_string(self):
        return self.data["username"] + "@" + self.data["hostname"]

    def get_catalina_home(self):
        return self.data["tomcat"]["home"]

    def get_tomcat_username(self):
        return self.data["tomcat"]["username"]

    def get_tomcat_password(self):
        return self.data["tomcat"]["password"]

    def get_tomcat_hostname(self):
        return self.data["hostname"]

    def get_tomcat_port(self):
        return self.data["tomcat"]["port"]

    def get_monit_home(self):
        return self.data["monit"]["home"]

    def get_tomcat_deploy_directory(self):
        dir = None
        if self.project_id in self.data["applications"]["n0"]:
            dir = self.data["tomcat"]["home"] + "/n0"
        elif self.project_id in self.data["applications"]["n1"]:
            dir = self.data["tomcat"]["home"] + "/n1"
        elif self.project_id in self.data["applications"]["n2"]:
            dir = self.data["tomcat"]["home"] + "/n2"

        if dir:
            return dir
        else:
            raise ProjectIdNotFoundException()
