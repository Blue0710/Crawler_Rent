from pymongo import MongoClient
from contextlib import contextmanager
from dotenv import load_dotenv
import logging
load_dotenv('.env')

logger = logging.getLogger(__name__)


@contextmanager
def mongo_con(host, port, collection, user=None, pwd=None):
    try:
        logger.info('Connecting MongoDB ...')
        client = MongoClient(host=host, port=port, username=user, password=pwd)
        logger.info('Authenticated!')
        # logger.info(client.server_info())
        db = client[collection]
        logger.info(f'Use collection: {db}')

        yield db
    finally:
        try:
            client.close()
        except Exception:
            pass
