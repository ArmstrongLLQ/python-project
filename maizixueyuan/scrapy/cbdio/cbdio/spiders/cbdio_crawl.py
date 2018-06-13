# -*- coding: utf-8 -*-
import scrapy
from cbdio.items import CbdioItem
import uuid

class CbdioCrawlSpider(scrapy.Spider):
    name = 'cbdio_crawl'
    allowed_domains = ['cbdio.com']
    start_urls = ['http://cbdio.com/']

    #获取网页数据
    # def start_requests(self):
    #     reqs = []
    #     for i in range(2, 30):
    #         req = scrapy.Request("http://www.cbdio.com/index_%s.html"%i)
    #         reqs.append(req)
    #     return reqs
    
    def parse(self, response):
        
        #一级页面需要获取的数据‘标题’、‘时间’、‘简介’
        titles = response.xpath('/html/body/div[6]/div[2]/div[1]/div[3]/ul/li/div/p[1]/a/text()').extract()
        times = response.xpath('/html/body/div[6]/div[2]/div[1]/div[3]/ul/li/div/p[2]/text()').extract()
        descriptions = response.xpath('/html/body/div[6]/div[2]/div[1]/div[3]/ul/li/div/p[3]/text()').extract()

        yield titles, times, descriptions
        
        
        #从一级页面获取二级页面的url，存入列表second_url  
        content_urls = response.xpath('/html/body/div[6]/div[2]/div[1]/div[3]/ul/li/div/p[1]/a/@href').extract()
        second_urls = []
        for each in content_urls:
            second_urls.append('http://www.cbdio.com/'+each)
        
    
        for title,time,description,second_url in zip(titles,times,descriptions,second_urls):
            item = CbdioItem()
            guid = uuid.uuid3(uuid.NAMESPACE_DNS, second_url)
            
            item['TITLE'] = title
            item['TIME'] = time
            item['DESCRIPTION'] = description
            item['GUID'] = guid
            item['SECOND_URL'] = second_url

        yield item


    #         yield scrapy.Request(url = item['SECOND_URL'], meta = {'item':item}, callback = self.parse_detail, dont_filter=True)

    # def parse_detail(self, response):


    #     item = response.meta['item']

    #     # item['SOURCE'] = response.css('body > div.am-container.cb-main > div.am-g > div.am-u-md-8 > div:nth-child(1) > p.cb-article-info > span:nth-child(1) > a:nth-child(2)::text').extract()
    #     # item['AUTHOR'] = response.css('body > div.am-container.cb-main > div.am-g > div.am-u-md-8 > div:nth-child(1) > p.cb-article-info > span:nth-child(3)::text').extract()
    #     # item['MAINTEXT'] = response.css('/html/body/div[4]/div[2]/div[1]/div[1]/p[2]::text').extract()

    #     item['SOURCE'] = response.xpath('//p[@class="cb-article-info"]/span[1]/text()').extract()[0]
    #     item['AUTHOR'] = response.xpath('//p[@class="cb-article-info"]/span[3]/text()').extract()[0]
    #     #item['MAINTEXT'] = response.css('/html/body/div[4]/div[2]/div[1]/div[1]/p[2]::text').extract()



    #     yield item