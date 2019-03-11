# -*- coding: utf-8 -*-
import scrapy
import time
import datetime

class ApachecamelspiderSpider(scrapy.Spider):
    name = 'ApacheCamelSpider'
    allowed_domains = ['issues.apache.org']
    start_urls = ['https://issues.apache.org/jira/browse/CAMEL-10597/']
	#setting the location of the output csv file
    
    def parse(self, response):		
		#Extract the labels of the detail section
        #details_lables=response.css('ul.property-list.two-cols strong.name::text').extract()
        details_lables=response.css('#issuedetails > li > div > strong::text').extract()
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
		#people_labels=response.css('div#peoplemodule.module dt::text').extract()
        #Extract the values of the people section
        people_values=response.xpath("//span[@class='user-hover']/text()").extract() 
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
        
		#TODO: get the epoch format of the date
        formatterDates =[]
        #for dateValue in dates_values:
        #   date_time_obj = datetime.datetime.strftime(dateValue, '%d/%b/%y %H:%M%')
        #  formatterDates.append(date_time_obj)	   
        #   formatterDates.append(date_time_obj.timestamp() * 1000 + ' ' + dateValue);		   
        print(formatterDates)
        newDateLabelList = []
        for date in dates_labels:
         newDateLabel=date.replace(':', '')
         newDateLabelList.append(newDateLabel)
         
        #extract comments
        comments_values=response.xpath('//*[@id="comment-15748543"]/div[1]/div[2]/p/text()').extract()
        commentsDict=dict(zip('comments', comments_values))
        print(comments_values)
        descriptionValues=response.css('div.user-content-block p::text').extract()
        descriptionValues=" ".join(descriptionValues)
        descrDict={'description' : descriptionValues}
        datesDict= dict(zip(newDateLabelList, dates_values))
        dicDetailsValue = dict(zip(labels_list, valueList))
        dicDetailsValue.update(datesDict)
        dicDetailsValue.update(peoplesDict)
        dicDetailsValue.update(commentsDict)
        dicDetailsValue.update(descrDict)
        scraped_info = dicDetailsValue
        #scraped_info = dict(zip(labels_list, peoplesDict))
        yield scraped_info