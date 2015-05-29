import logging


def getLogger(loglevel="INFO", appname="deploy"):
    logging.basicConfig(level=logging.getLevelName(loglevel), format="%(message)s")
    return logging.getLogger(appname)
