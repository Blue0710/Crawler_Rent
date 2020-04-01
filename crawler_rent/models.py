import time
import logging
# from itertools import chain
logger = logging.getLogger(__name__)


class RentCrawler:

    def __init__(self, base_url):
        self.base_url = base_url
        self.crawler_name = self.__class__.__name__

    def upsert_house(self, region, db, collection, key='_id', sleep_sec=None):
        logger.info(f'[{self.crawler_name}] Start crawling:')
        house_dict = self._crawl(region)
        start = time.time()
        for house in house_dict:
            logger.info(f'[{self.crawler_name}] Upsert {house["_id"]}: {house["url"]} ...')
            house_key = house[key]
            # card.update({"_id": card_key})

            timestamp = self._is_exist(db, collection, house['_id'], house['update_time'])
            if not timestamp:
                house['first_seen_date'] = house['update_time']
            else:
                house['first_seen_date'] = timestamp
            db[collection].replace_one({key: house_key}, house, upsert=True)

            if sleep_sec:
                time.sleep(sleep_sec)
        total = time.time() - start
        logger.info(f'[{self.crawler_name}] crawling time:{total}')

    def _is_exist(self, db, collection, id, timestamp_key='first_seen_date'):  # naming method for checking item is exist or not
        doc = db[collection].find_one({"_id": id})
        if doc:
            return doc['first_seen_date']

    def _crawl(self):
        # raise NotImplementedError
        print('here')
        pass
