from time import sleep
from commands import run
from commands import puts
from commands import put
from commands import abort

import urllib2
import base64


class Tomcat:
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

        abort("Can not complete the server startup")

    def shutdown(self):
        run(self.home + "/bin/shutdown.sh -force")

    def deploy(self, appname, warfile):
        run("rm -rf " + self.home + "/work")
        run("rm -rf " + self.home + "/webapps/" + appname)
        put(local_path=warfile, remote_path=self.deploy_dir)

    def _running(self):
        try:
            request = urllib2.Request("http://%s:%s/manager/text/list" % self.host, self.port)
            base64string = base64.encodestring('%s:%s' % (self.user, self.password))
            request.add_header("Authorization", "Basic %s" % base64string)
            data = urllib2.urlopen(request).read()

            return data[:4] == "OK -"
        except:
            return False
