# -*- coding: utf-8 -*-
import scrapy


class ApachecamelspiderSpider(scrapy.Spider):
    name = 'ApacheCamelSpider'
    allowed_domains = ['issues.apache.org']
    start_urls = ['https://issues.apache.org/jira/browse/CAMEL-10597/']
    #setting the location of the output csv file
    
    def parse(self, response):
        #Extract data using css selectors
        #details_row_data=response.xpath("//*[@id='peopledetails']/li[@class='people-details']/dl/text()").extract() 
        details_row_data=response.css('ul.property-list.two-cols strong.name::text').extract()
        
        #for item in details_row_data:
        #row_data=zip(details_row_data)
		
        #Making extracted data row wise
        for item in details_row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                'Person' : item #item[0] means product in the list and so on, index tells what value to assign, here for testing we have only one
            }

            #yield or give the scraped info to scrapy
            yield scraped_info
