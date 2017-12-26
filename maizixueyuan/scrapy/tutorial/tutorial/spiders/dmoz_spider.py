# -*- coding: utf-8 -*-
import scrapy


class DmozSpiderSpider(scrapy.Spider):
    name = "dmoz_spider"
    allowed_domains = ["dmoz.org"]
    start_urls = ['http://dmoz.org/']

    def parse(self, response):
        pass
