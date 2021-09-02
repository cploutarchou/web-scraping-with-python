import logging
from app import config
import graypy


def get_logger():
    """
    Setup the logger
    """
    logger = logging.getLogger('Stackoverflow Scraper')
    logger.setLevel(logging.INFO)

    handler = graypy.GELFTCPHandler('172.21.0.35', 12201)
    logger.addHandler(handler)
    return logger


