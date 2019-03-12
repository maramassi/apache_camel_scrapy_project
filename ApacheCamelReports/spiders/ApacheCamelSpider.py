# -*- coding: utf-8 -*-
import scrapy
import datetime
from datetime import datetime as dt

class ApachecamelspiderSpider(scrapy.Spider):
    
    name = 'ApacheCamelSpider'
    allowed_domains = ['issues.apache.org']
    start_urls = ['https://issues.apache.org/jira/browse/CAMEL-10597/']
	#setting the location of the output csv file
    
	#local functions to be used
	
    def parse(self, response):	

        #function used to get the epoch date from the datetime
        def epochDate(date_time_str):
           date_time_obj = dt.strptime(date_time_str, '%d/%b/%y %H:%M').timestamp()
           return date_time_obj

        #function used to get rid of the spaces, carriage returns, etc.. of the strings
        def clearStringList(strListToClear):
           newClearedList=[]
           for details in strListToClear:
            newDetail=details.replace(':', '').replace('\n', '').replace('\r', '').replace(' ','')
            newClearedList.append(newDetail)
           return newClearedList
		   
		#Extract the labels of the detail section
        #details_lables=response.css('ul.property-list.two-cols strong.name::text').extract()
        details_lables=response.css('#issuedetails > li > div > strong::text').extract()
        details_lables= clearStringList(details_lables)
		 
		#Extract the values of the details section. TODO
        details_values=response.css('#issuedetails span.value > span::text').extract() 
        valueList=[]
        for value in details_values:
         new=value.replace('\n', '').replace('\r', '').replace(' ','')
         valueList.append(new)

        #Extract the Labels of the people section
        people_labels=response.css('ul#peopledetails li.people-details dt::text').extract()
        people_labels=clearStringList(people_labels)
        
		#Extract the values of the people section
        #people_values=response.xpath("//span[@class='user-hover']/text()").extract() 
        people_values=response.css('span.view-issue-field span.user-hover::text').extract() 
        people_values=clearStringList(people_values)
        
        #dates section
        dates_labels=response.css('div#datesmodule.module > div.mod-content ul li dl.dates dt::text').extract()
        dates_values=response.css('dd.date time.livestamp::text').extract()
        
        #TODO: get the epoch format of the date
        epochDates =[]
        for dateValue in dates_values:
          epochDates.append(epochDate(dateValue))	   
        print("formatted dates")         
        print(epochDates)
        newDateLabelList = []
        for date in dates_labels:
         newDateLabel=date.replace(':', '')
         newDateLabelList.append(newDateLabel)
         
        #extract comments section
        comments_values=response.xpath('//*[@id="comment-15748543"]/div[1]/div[2]/p/text()').extract()
        commentsDict=dict(zip('comments', comments_values))

		#extract description section
        descriptionValues=response.css('div.user-content-block p::text').extract()
        descriptionValues=" ".join(descriptionValues)

		#building the dictionnaries
        descrDict={'description' : descriptionValues}
        datesDict= dict(zip(newDateLabelList, epochDates))
        peoplesDict= dict(zip(people_labels, people_values))
        dicDetailsValue = dict(zip(details_lables, valueList))
        dicDetailsValue.update(datesDict)
        dicDetailsValue.update(peoplesDict)
        dicDetailsValue.update(commentsDict)
        dicDetailsValue.update(descrDict)
        
        scraped_info = dicDetailsValue

        yield scraped_info