import logging

from colors import Colors

class ShipLogger:
    def __init__(self, loglevel):
        logging.basicConfig(level=logging.getLevelName(loglevel), format="%(message)s")
        self.logger = logging.getLogger("ship")

    @staticmethod
    def get_logger(loglevel="INFO"):
        return ShipLogger(loglevel)

    def info(self, msg):
        self.logger.info(Colors.OKGREEN + msg + Colors.ENDC)

    def warning(self, msg):
        self.logger.warning(Colors.WARNING + msg + Colors.ENDC)

    def error(self, msg):
        self.logger.error(Colors.FAIL + msg + Colors.ENDC)

    def success(self, msg):
        self.logger.error(Colors.OKBLUE + msg + Colors.ENDC)
