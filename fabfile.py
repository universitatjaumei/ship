from fabric.api import task
from tomcat import Tomcat


@task
def deploy(app, home, user, password):
    tomcat = Tomcat(home, user, password)
    tomcat.shutdown()
    tomcat.deploy(app)
    tomcat.startup()
