import logging
import sys
from colors import Colors

class ShipLogger:
    def __init__(self, loglevel):
        self.logger = logging.getLogger("ship")
        if  not self.logger.handlers:
            self._setup_logger(loglevel)

    def _setup_logger(self, loglevel, fmt="[ship] %(levelname)s %(message)s"):
        logging.basicConfig(format=fmt)
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(fmt))
        self.logger.addHandler(handler)

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
