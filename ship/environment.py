import yaml

class Environment:
    def __init__(self, app):
        f = open('environment.yml')
        data = yaml.safe_load(f)
        f.close()

        self.app = app
        self.config = data[app]

    def get_remote_connection_string(self):
        return self.config["user"] + "@" + self.config["host"]

    def get_remote_host(self):
        return self.config["host"]

    def get_remote_port(self):
        return self.config["port"]

    def get_tomcat_host(self):
        return self.config["tomcat"]["host"]

    def get_tomcat_version(self):
        return self.config["tomcat"]["version"]

    def get_tomcat_base(self):
        return self.config["tomcat"]["base"]

    def get_tomcat_home(self):
        return self.get_tomcat_base() + "/" + "apache-tomcat-" + self.get_tomcat_version()

    def get_tomcat_memory(self):
        value = self.config["tomcat"]["memory"]
        return "-Xmx%sM -Xms%sM" % (value, value)

    def get_tomcat_username(self):
        return self.config["tomcat"]["username"]

    def get_tomcat_password(self):
        return self.config["tomcat"]["password"]

    def get_tomcat_http_port(self):
        return self.config["tomcat"]["ports"]["http"]

    def get_tomcat_ajp_port(self):
        return self.config["tomcat"]["ports"]["ajp"]

    def get_tomcat_jmx_port(self):
        return self.config["tomcat"]["ports"]["jmx"]

    def get_tomcat_shutdown_port(self):
        return self.config["tomcat"]["ports"]["shutdown"]

    def get_tomcat_redirect_port(self):
        return self.config["tomcat"]["ports"]["redirect"]

    def get_tomcat_deploy_directory(self):
        return self.get_tomcat_home() + "/webapps"

    def get_monit_home(self):
        return self.config["monit"]["home"]
