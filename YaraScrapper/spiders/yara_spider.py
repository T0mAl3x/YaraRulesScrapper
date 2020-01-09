# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class YaraSpiderSpider(CrawlSpider):
    name = 'yara_spider'
    start_urls = ['https://github.com/Yara-Rules/rules/']

    custom_settings = {
        'CONCURRENT_REQUESTS': 24,
        'REACTOR_THREADPOOL_MAXSIZE': 24,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
        'DEPTH_PRIORITY': 8,
        'DOWNLOAD_TIMEOUT': 90,
        'RETRY_TIMES': 1,
        'MAX_PAGES_PER_DOMAIN': 1500,
        'RETRY_HTTP_CODES': []
    }

    rules = (
        Rule(LinkExtractor(allow='rules/tree', restrict_xpaths=[
            './/td[@class="content"]'
        ], unique=True)),
        Rule(LinkExtractor(allow=r'\.yar', unique=True), callback='parse_item')
    )

    def parse_item(self, response):
        yield {
            'url': response.url
        }
