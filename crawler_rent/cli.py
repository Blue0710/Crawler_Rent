from .io import mongo_con
from .crawlers.rent591 import (
    Rent591Crawler
)

from .config import URL_DICT
import click
import os
from logging import getLogger
logger = getLogger(__name__)

# Variables of mongodb
MONGODB_HOST = os.environ.get("MONGODB_HOST", "")
MONGODB_PORT = int(os.environ.get("MONGODB_PORT", ""))
MONGODB_DB = os.environ.get("MONGODB_DB", "")
MONGODB_USER = os.environ.get("MONGODB_USER", "")
MONGODB_PWD = os.environ.get("MONGODB_PWD", "")

MONGODB_RENT_COLLECTION = os.environ.get("MONGODB_RENT_COLLECTION", 'rent_house')
# MONGODB_CAMPAIGN_COLLECTION = os.environ.get("MONGODB_CAMPAIGN_COLLECTION", 'card_campaigns')

# BANK_LIST = ['taishin', 'cathay', 'esun']

# ['taishin', 'cathay', 'esun', 'all]
card_crawler_map = {
    "591_rent": Rent591Crawler(URL_DICT['rent591']['region_url']),
}


@click.command()
@click.option("-r", "--region",
              type=click.Choice(['台北市', '基隆市', '新北市', '新竹市', '新竹縣', '桃園市', '苗栗縣', '台中市', '彰化縣', '南投縣', '嘉義市', '嘉義縣', '雲林縣', '台南市', '高雄市', '屏東縣', '宜蘭縣', '台東縣', '花蓮縣', '澎湖縣', '金門縣', '連江縣', "all"], case_sensitive=False),
              multiple=True,
              help="Specify region (e.g, `-r '宜蘭縣'` or ˋ-r '台北市' -r '新北市'ˋ)",
              default="all", required=True)  # default="all", show_default=True)
# @click.option("-t", "--types",
#               type=click.Choice(["card", "campaign", "all"], case_sensitive=False),
#               default="all", required=True)
def main(region):
    '''Crawling Specify region '''
    logger.info(f"Crawling -- region: {region}")

    if region == "all":
        region = ['台北市', '基隆市', '新北市', '新竹市', '新竹縣', '桃園市', '苗栗縣', '台中市', '彰化縣', '南投縣', '嘉義市', '嘉義縣', '雲林縣', '台南市', '高雄市', '屏東縣', '宜蘭縣', '台東縣', '花蓮縣', '澎湖縣', '金門縣', '連江縣']
    else:
        region = list(region)
    logger.info(f"get：{region}")
    house_jobs = [f"{r}" for r in region]  # ['taishin_card', 'cathay_card']

    with mongo_con(MONGODB_HOST, MONGODB_PORT, MONGODB_DB, MONGODB_USER, MONGODB_PWD) as db:
        # if 'card' in types:
        for job in house_jobs:
            card_crawler_map["591_rent"].upsert_house(
                job, db, MONGODB_RENT_COLLECTION, key="_id")


if __name__ == "__main__":
    main()
