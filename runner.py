from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroyparcing import settings
from leroyparcing.spiders.leroy import LeroySpider
from pymongo import MongoClient

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    searchInput = 'плитка'

    process.crawl(LeroySpider, searchInput=searchInput)
    process.start()
