import logging

class Logger():
    def __init__(self):
        #Example:
        #2025-11-03 20:29:28 | INFO | main.py:29 >>> Some log
        LOG_FORMAT = '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d >>> %(message)s'
        DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

        logging.basicConfig(
            level=logging.INFO,
            format=LOG_FORMAT,
            datefmt=DATE_FORMAT,
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )

        INIT_LEVEL = 25  # between INFO (20) and WARNING (30)
        logging.addLevelName(INIT_LEVEL, "INIT")

        def init(self, message, *args, **kwargs):
            if self.isEnabledFor(INIT_LEVEL):
                self._log(INIT_LEVEL, message, args, **kwargs) #base logging .log function called with custom log level

        # add INIT method to Logger class
        logging.Logger.init = init

        logging.getLogger(__name__).init("Logging initialized")