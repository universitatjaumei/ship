import yaml

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

    def get_remote_connection_string(self):
        return self.data["user"] + "@" + self.data["host"]

    def get_remote_host(self):
        return self.data["host"]

    def get_remote_port(self):
        return self.data["port"]

    def get_catalina_home(self):
        return self.data["tomcat"]["home"]

    def get_tomcat_username(self):
        return self.data["tomcat"]["user"]

    def get_tomcat_password(self):
        return self.data["tomcat"]["password"]

    def get_tomcat_hostname(self):
        return self.data["tomcat"]["host"]

    def get_tomcat_port(self):
        return self.data["tomcat"]["port"]

    def get_monit_home(self):
        return self.data["monit"]["home"]

    def get_tomcat_deploy_directory(self):
        return self.data["tomcat"]["home"] + "/webapps"
