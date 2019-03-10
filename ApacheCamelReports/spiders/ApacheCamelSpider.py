# -*- coding: utf-8 -*-
import scrapy


class ApachecamelspiderSpider(scrapy.Spider):
    name = 'ApacheCamelSpider'
    allowed_domains = ['issues.apache.org']
    start_urls = ['https://issues.apache.org/jira/browse/CAMEL-10597/']
	#setting the location of the output csv file
    
    def parse(self, response):
        #Extract the labels of the detail section
        details_lables=response.css('ul.property-list.two-cols strong.name::text').extract()
        labels_list=[]        
        for value in details_lables:
         new=value.replace(':', '')
         labels_list.append(new)		 
		 
        #Extract the values of the details section. TODO
        details_values=response.css('div.value.type-select, div.shorten span, span.labels, span#components-val.value a, span.shorten span, span > ::text').extract()
        valueList=[]
        for value in details_values:
         new=value.replace('\n', '').replace('\r', '').replace(' ','')
         valueList.append(new)

		
        #Extract the Labels of the people section
        people_labels=response.css('div#peoplemodule.module dt::text').extract()
        #Extract the values of the people section
        people_values=response.css('div#peoplemodule.module dd > span::text').extract()
        #Extract the values of the people section
        dates_values=response.css('div#datesmodule.module div.mod-content dl.dates').extract() 
        #extract comments
        #comments_values=response.css('div#comment-15748543.issue-data-block div.action-body').extract()
        scraped_info = dict(zip(labels_list, valueList))
        yield scraped_info
        #lenList = len(details_lables)
        #print("the lenght of the array")
        #print(lenList)
        #for item in details_lables:
            #create a dictionary to store the scraped info
        #    scraped_info = {
        #     'a': item,
             #'b': item[1]#: details_row_value[0] #item[0]
        #    }
            #yield or give the scraped info to scrapy
        #    yield scraped_info
