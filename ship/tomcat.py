import urllib2

from logger import ShipLogger
from time import sleep
from commands import *

class Tomcat:
    logger = ShipLogger.get_logger("INFO")

    def __init__(self, catalina_home, adm_user, adm_password, tomcat_host, tomcat_port, deploy_dir):
        self.home = catalina_home
        self.user = adm_user
        self.password = adm_password
        self.host = tomcat_host
        self.port = tomcat_port
        self.deploy_dir = deploy_dir

    def startup(self):
        run(self.home + "/bin/startup.sh")

        times = 1

        while not self._running() and times < 30:
            sleep(10)
            puts(".")
            times = times + 1

        if times == 30:
            error_message = "Can not complete the server startup"
            abort(error_message)
            self.logger.error(error_message)

        self.logger.info("Tomcat startup process completed")

    def shutdown(self):
        run(self.home + "/bin/shutdown.sh -force")

    def deploy(self, module):
        appname = module.get_name()
        warfile = "%s/target/%s.war" % (module.get_directory(), appname)

        run("rm -rf " + self.home + "/work")
        run("rm -rf " + self.home + "/webapps/" + appname)
        put(local_path=warfile, remote_path=self.deploy_dir)

    def _running(self):
        try:
            url = "http://%s:%s/manager/text/list" % (self.host, self.port)
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, url, self.user, self.password)

            urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

            request = urllib2.Request(url)
            data = urllib2.urlopen(request).read()

            return data[:4] == "OK -"
        except:
            return False