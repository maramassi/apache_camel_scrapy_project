# -*- coding: utf-8 -*-
import scrapy


class ApachecamelspiderSpider(scrapy.Spider):
    name = 'ApacheCamelSpider'
    allowed_domains = ['issues.apache.org']
    start_urls = ['https://issues.apache.org/jira/browse/CAMEL-10597/']
	#setting the location of the output csv file
    
    def parse(self, response):
	    #Extract data using css selectors
        title=response.css('.toggle-title::text').extract()
        row_data=zip(title)
		
        #Making extracted data row wise
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                #key:value
                'page':response.url,
                'title' : item[0], #item[0] means product in the list and so on, index tells what value to assign, here for testing we have only one
            }

            #yield or give the scraped info to scrapy
            yield scraped_info
