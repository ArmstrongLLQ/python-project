# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CbdioItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    GUID = scrapy.Field()
    TITLE = scrapy.Field()
    TIME = scrapy.Field()
    DESCRIPTION = scrapy.Field()
    SECOND_URL = scrapy.Field()
    # AUTHOR = scrapy.Field()
    # SOURCE = scrapy.Field()
