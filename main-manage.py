#!/usr/bin/python2

import traceback

from ship.logger import ShipLogger
from ship.environment import Environment
from ship.tomcat import Tomcat
from ship.commands import set_environment

if __name__ == "__main__":
    logger = ShipLogger("INFO")

    try:
        app = "sample"

        config = Environment(app)
        set_environment(config)

        tomcat = Tomcat(config)
        tomcat.uninstall()
        tomcat.install()

        logger.success("Finished succesfully!!")
    except Exception as e:
        print traceback.format_exc()
