import logging

from Log.LogHandle import LogHandle

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = LogHandle()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

loggers = [logger, logging.getLogger('sqlalchemy')]

for l in loggers:
    l.addHandler(ch)
if __name__ == '__main__':
    logger.info("test")
