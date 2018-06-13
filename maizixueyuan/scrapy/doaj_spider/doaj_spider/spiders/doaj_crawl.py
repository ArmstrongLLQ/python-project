# -*- coding: utf-8 -*-
import scrapy


class DoajCrawlSpider(scrapy.Spider):
    name = 'doaj_crawl'
    allowed_domains = ['http://121.42.164.187:8088/']
    start_urls = ['http://http://121.42.164.187:8088//']

    def parse(self, response):
        pass
