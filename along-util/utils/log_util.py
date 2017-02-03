import logging

class Log(object):
    def __init__(self):
        logging.basicConfig(filename='myapp.log',level=logging.DEBUG)
        pass

    @staticmethod
    def debug(msg):
        logging.debug(msg)
    
    @staticmethod
    def info(msg):
        logging.info(msg)
    
    @staticmethod
    def log(msg):
        Log.info(msg)

    @staticmethod
    def error(msg):
        log.error(msg)

