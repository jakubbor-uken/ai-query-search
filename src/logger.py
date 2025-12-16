import logging

# example: 2025-11-03 20:29:28 | INFO | main.py:29 >>> Some log
LOG_FORMAT = '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d >>> %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
INIT_LEVEL = 25  # numeric logging level of our custom INIT level,
                 # placed between INFO (20) and WARNING (30),
                 # greater numbers represent higher priority


class Logger:
    """Class responsible for registering logs.

    It wraps the Logger class from python standard library logging module.
    This is for the sake of convenience because desired configuration is known beforehand
    and does not alter through the course of running this program. Thus, it can be hard-coded
    and encapsulated. Configuration consists of specifying log format, and also adding another
    level for our needs. This is INIT, which is utilized in initializations of classes
    that our program consists of.
    """
    def __init__(self):

        logging.basicConfig(
            level=logging.INFO,
            format=LOG_FORMAT,
            datefmt=DATE_FORMAT,

            # where should logs be passed
            handlers=[
                logging.FileHandler('app.log'),  # file to hold logs
                logging.StreamHandler()          # stderr will also receive logs
            ]
        )

        # We add our custom INIT level
        logging.addLevelName(INIT_LEVEL, "INIT")

        def init(self, message, *args, **kwargs):
            if self.isEnabledFor(INIT_LEVEL):
                # base logging .log function called with custom log level
                self._log(INIT_LEVEL, message, args, **kwargs)

        # add INIT method to Logger class
        logging.Logger.init = init

        # At the end, we report initialization complete
        logging.getLogger(__name__).init("Logging initialized")
