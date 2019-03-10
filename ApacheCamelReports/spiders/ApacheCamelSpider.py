# -*- coding: utf-8 -*-
import scrapy


class ApachecamelspiderSpider(scrapy.Spider):
    name = 'ApacheCamelSpider'
    allowed_domains = ['https://issues.apache.org/jira/browse/CAMEL-10597']
    start_urls = ['http://https://issues.apache.org/jira/browse/CAMEL-10597/']

    def parse(self, response):
        pass
