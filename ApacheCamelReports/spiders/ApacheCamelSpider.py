# -*- coding: utf-8 -*-
import scrapy
import datetime
from datetime import datetime as dt

class ApachecamelspiderSpider(scrapy.Spider):
    
    name = 'ApacheCamelSpider'
    allowed_domains = ['issues.apache.org']
    start_urls = ['https://issues.apache.org/jira/browse/CAMEL-10597/']
	 
    def parse(self, response):	

        #function used to get the epoch date from the datetime
        def epochDate(date_time_list):
           date_epoch_list=[]
           #loop on the list of dates => convert it to milliseconds format
           for date_time_str in date_time_list:
             #date_time_obj = dt.strptime(date_time_str, '%d/%b/%y %H:%M').timestamp()
             date_time_obj = dt.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S%z').timestamp()
             date_epoch_list.append(date_time_obj)
           return date_epoch_list
	   
		#function used to get the epoch date lables. Derived from the date Labels by adding the suffix _Epoch   
        def epochDateLabels(dateLabelsList):
           newList=[]
           for label in dateLabelsList:
            newList.append(label + "_Epoch")
           return newList

		#function used to get rid of the spaces, carriage returns, etc.. of the list of strings
        def clearStringList(strListToClear):
           newClearedList=[]
           for details in strListToClear:
            newDetail=details.replace(':', '').replace('\n', '').replace('\r', '').strip()
            newClearedList.append(newDetail)
           return newClearedList
		 
        #DETAILS section: extracting all the li-details items		 
        detailsItems =response.xpath("//ul[@class='property-list']/li[starts-with(@class, 'item')]") 
        
		#extracting the labels of the details section
        details_lables=clearStringList(detailsItems.xpath("//div[@class='wrap']/strong/text()").extract())
        
        #this list will contain the extracted values of the details section
        details_values=[]
        
		#looping on the unordered list to get all the liste items
        for liItem in response.css('ul.property-list > li.item > div.wrap'):
		  #for the fixVersions field, we need to concatenate the values of the versions
          if liItem.css('*#fixVersions-field'):
            versionsList = liItem.xpath('span[@id="fixfor-val"]/span/a/text()').extract()
            versionsListStr=", ".join(versionsList)
            details_values.append(versionsListStr)
          else:
            #todo: check descendant
            details_values.append(liItem.xpath('span/text()[not(normalize-space(.)="")] | span/*/text()[not(normalize-space(.)="")] | span/span/*/text() | div/*/text()  | div/div/*/text() | div/text()[not(normalize-space(.)="")] | div/div[@id="shorten"]/span/text()[not(normalize-space(.)="")]').extract_first())
            
		#parsing the people section fields. The first span is always an image for both the Assignee and the Reporter => Select the second element
        peopleLables=response.xpath('//div[@id="peoplemodule"]//ul[@class="item-details"]//dt/text()[not(normalize-space(.)="")]').extract()
        peopleValueList=clearStringList(response.xpath('//div[@id="peoplemodule"]//ul[@class="item-details"]//span[contains(@class, "user-hover") or contains(@class, "aui-badge")]/text()[not(normalize-space(.)="")]').extract())
        
        #dates section. Get the list of all the fields in the date section as well as their values
        dates_labels=clearStringList(response.css('div#datesmodule.module > div.mod-content ul li dl.dates dt::text').extract())
        dates_values=response.css('dd.date time.livestamp::attr(datetime)').extract()
		#get the epoch format of the date
        epochDates = epochDate(dates_values)
                 
        #extract description section
        descriptionValues=response.css('#description-val div.user-content-block p::text, #description-val div.user-content-block .codeContent *::text').extract()
        #combine all the parsed description into a single field
        descriptionValues=" ".join(descriptionValues)

		#TODO extract comments section //*[@class="activity-comment"]/div[1]/div[2]/p/text()
		#description with code part response.css('.mod-content * p::text, .mod-content * span::text').extract() 
        comments_values=response.css('div.issue-data-block.focused p:nth-of-type(1)').extract() 
        comments_values1= response.xpath('//*[@id="comment-15748543"]/div[1]/div[2]/p/text()').getall()
        print('***********CMT***************')
        print(comments_values)
        #combine all the parsed comments into a single field
        comments_values=" ".join(comments_values)
				
		#building the dictionnaries
        #combining the dictionnaries into a global one
        descrDict={'description' : descriptionValues} #key : value
        commentsDict={'comments' : comments_values}
        datesDict= dict(zip(dates_labels, dates_values))
        datesEpochDict=dict(zip(epochDateLabels(dates_labels),epochDates))
        dicDetailsValue = dict(zip(details_lables, clearStringList(details_values)))
        peopleDict = dict(zip(peopleLables, peopleValueList))
        dicDetailsValue.update(datesDict)
        dicDetailsValue.update(datesEpochDict)
        dicDetailsValue.update(peopleDict)
        dicDetailsValue.update(commentsDict)
        dicDetailsValue.update(descrDict)
        
        scraped_info = dicDetailsValue

        yield scraped_info