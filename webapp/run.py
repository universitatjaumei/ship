from ship.logger import ShipLogger
from ship.project import ProjectBuilder
from ship.validator import *
from ship.errors import SVNException, ProjectIdNotFoundException
from flask import Flask, request, render_template
import urllib2
import yaml
import simplejson
import traceback

app = Flask(__name__)

ENVIRONMENT = "production"
HOME = "/tmp/target"
URL = "svn://ship-svn/repos/SAMPLE"
PROJECT_NAME = "sample"
KEY = "smp"
VERSION = "trunk"

@app.route("/deploy", methods=["POST"])
def hello():
    environment = request.args.get("environment") #"production"
    home = request.args.get("home") #"/tmp/target"
    url = request.args.get("url") #"svn://localhost/repos/SAMPLE"
    project = request.args.get("project") #"sample"
    key = request.args.get("key") #"smp"
    version = request.args.get("version") #"trunk"

    try:
        app.logger.info("Initializing project construction")

        rules = [ ConfigFileValidationRule, ConsoleLogValidationRule,
                  PomXMLValidationRule, CompiledPackageExistsValidationRule ]

        project = ProjectBuilder(HOME, PROJECT_NAME, "/etc/uji/%s/app.properties" % KEY) \
            .with_subversion(URL, VERSION) \
            .with_maven() \
            .with_validation_rules(rules) \
            .build() \
            .deploy(ENVIRONMENT)

        app.logger.info("Finished succesfully!!")
    except SVNException as e:
        app.logger.error("Invalid or unauthorized SVN repository '" + PROJECT_NAME + "'")
        return "fail :("

    except ProjectIdNotFoundException as e:
        app.logger.error("ProjectID not found in Tomcat")
        return "fail :("

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return "fail :("

    return  "ole :)"


@app.route("/", methods=["GET"])
def index():
    apps = [ 'SAMPLE' ]
    return render_template("index.html", apps=apps)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
