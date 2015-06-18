from commands import *
from time import sleep
import os.path
import re


class Monit:

    def __init__(self, home):
        self.home = home

    def get_deploy_directory(self, service_name):
        return os.path.join(self.home, service_name, service_name + ".jar")

    def startup_service(self, name):
        run("sudo /usr/bin/monit start " + name)

        times = 1
        while not self._running(name) and times < 30:
            sleep(10)
            puts(".")
            times = times + 1

        if not self._running(name):
            abort("Can not complete the service '%s' startup" % name)

    def shutdown_service(self, name):
        run("sudo /usr/bin/monit stop " + name)

    def deploy(self, jarfile, name):
        put(local_path=jarfile, remote_path=self.get_deploy_directory(name))

    def _running(self, name):
        res = run("sudo /usr/bin/monit status")
        res = res.split("\r\n")
        index = res.index("Process '%s'" % name)
        status = res[index + 1].strip()
        status = re.sub(' +', ' ', status)

        return status.split()[1] == 'running'


if __name__ == "__main__":
    from environment import Environment
    deploy_environment = Environment("development", "uji-ade-bd2storage")
    set_environment(deploy_environment)
    monit = Monit("/mnt/data/aplicacions/cron/")
    print monit._running("uji-ade-bd2storage")
    monit.shutdown_service("uji-ade-bd2storage")
    monit.deploy(
        "/opt/devel/workspaces/uji/uji-deployment-tools/deploy/target/ADE/uji-ade/uji-ade-bd2storage/target/uji-ade-bd2storage.jar", "uji-ade-bd2storage")
    monit.startup_service("uji-ade-bd2storage")
