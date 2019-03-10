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
        #removing the : from the labels
        labels_list=[]        
        for details in details_lables:
         newDetail=details.replace(':', '')
         labels_list.append(newDetail)		 
		 
        #Extract the values of the details section. TODO
        details_values=response.css('#issuedetails span.value::text').extract()
        valueList=[]
        for value in details_values:
         new=value.replace('\n', '').replace('\r', '').replace(' ','')
         valueList.append(new)

        #Extract the Labels of the people section
        people_labels=response.css('ul#peopledetails li.people-details dt::text').extract()
        #removing the : from the labels
        peopleLabelList=[]
        for value in people_labels:
         newPeople=value.replace(':', '')
         peopleLabelList.append(newPeople)
	
	#Extract the values of the people section
        people_values=response.css('#issue_summary_assignee_davsclaus:nth-child(1)::text').extract() 
        peopleList=[]
        for people in people_values:
         newPeopleVal=people.replace('\n', '').replace('\r', '').replace(' ','')
         peopleList.append(newPeopleVal)
        print(peopleList)
        peoplesDict= dict(zip(peopleLabelList, peopleList))
        #response.css('div#peoplemodule.module dd > span::text').extract()
        print(peoplesDict)
        #dates section
        dates_labels=response.css('div#datesmodule.module > div.mod-content ul li dl.dates dt::text').extract()
        dates_values=response.css('dd.date time.livestamp::text').extract()
        newDateLabelList = []
        for date in dates_labels:
         newDateLabel=date.replace(':', '')
         newDateLabelList.append(newDateLabel)
         
        #extract comments
        #comments_values=response.css('div#comment-15748543.issue-data-block div.action-body').extract()
        datesDict= dict(zip(newDateLabelList, dates_values))
        dicDetailsValue = dict(zip(labels_list, valueList))
        dicDetailsValue.update(datesDict)
        dicDetailsValue.update(peoplesDict)
        scraped_info = dicDetailsValue
        #scraped_info = dict(zip(labels_list, peoplesDict))
        yield scraped_info
