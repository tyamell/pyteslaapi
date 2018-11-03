#!/usr/bin/python
"""
Tesla CLI
"""

from client import TeslaApiClient
from exceptions import TeslaException
import logging

_LOGGER = logging.getLogger('pyteslaapi_cli')


def setup_logging(log_level=logging.INFO):
    """Set up the logging."""
    logging.basicConfig(level=log_level)
    fmt = ("%(asctime)s %(levelname)s (%(threadName)s) "
           "[%(name)s] %(message)s")
    colorfmt = "%(log_color)s{}%(reset)s".format(fmt)
    datefmt = '%Y-%m-%d %H:%M:%S'

    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    try:
        from colorlog import ColoredFormatter
        logging.getLogger().handlers[0].setFormatter(ColoredFormatter(
            colorfmt,
            datefmt=datefmt,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            }
        ))
    except ImportError:
        pass

    logger = logging.getLogger('')
    logger.setLevel(log_level)

def call():
    """Execute command line helper."""

    log_level = logging.DEBUG


    setup_logging(log_level)
    try:
        api = TeslaApiClient("tyamell@gmail.com","T1aB2stsp!ez142215")
        vehicles = api.vehicles


        for v in vehicles:
            if not v.wake_up():
                _LOGGER.error("Unable to wake up vehicle")
                continue
            v.update()
            _LOGGER.info(v.drive.attributes)
            _LOGGER.info(v.climate.attributes)
            _LOGGER.info(v.charge.attributes)
            _LOGGER.info(v.gui_settings.attributes)
            _LOGGER.info(v.locked)
    except TeslaException as exc:
        _LOGGER.error(exc.message)



def main():
    """Execute from command line."""
    call()



if __name__ == '__main__':
    main()
