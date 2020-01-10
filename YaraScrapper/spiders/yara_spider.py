# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from YaraScrapper.items import YarascrapperItem
from urllib.parse import urlparse


class YaraSpiderSpider(CrawlSpider):
    name = 'yara_spider'
    start_urls = ['https://github.com/Yara-Rules/rules/']

    custom_settings = {
        'CONCURRENT_REQUESTS': 10,
        'REACTOR_THREADPOOL_MAXSIZE': 10,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DEPTH_PRIORITY': 8,
        'DOWNLOAD_TIMEOUT': 90,
        'DOWNLOAD_DELAY': 0.25,
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
        relative_url = response.xpath('//a[@id="raw-url"]/@href').extract_first()
        absolute_url = response.urljoin(relative_url)
        yield Request(absolute_url, callback=self.download_item)

    def download_item(self, response):
        loader = ItemLoader(item=YarascrapperItem(), )
        loader.add_value('file_urls', response.url)
        name = urlparse(response.url).path.split("/")[-1]
        loader.add_value('file_name', name)
        yield loader.load_item()
