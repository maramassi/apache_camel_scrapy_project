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
             date_time_obj = dt.strptime(date_time_str, '%d/%b/%y %H:%M').timestamp()
             date_epoch_list.append(date_time_obj)
           return date_epoch_list

        def isoTimeFormat(date_time_list):
           date_iso_list=[]
           #loop on the list of string dates => convert it from string format => convert it to isoformat
           for date_time_str in date_time_list:
             date_time_obj = dt.strptime(date_time_str, '%d/%b/%y %H:%M')
             date_iso_list.append(date_time_obj.isoformat(timespec='microseconds'))
           return date_iso_list		
		   
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
            newDetail=details.replace(':', '').replace('\n', '').replace('\r', '').replace(' ','')
            newClearedList.append(newDetail)
           return newClearedList
		  
		#Extract the labels of the detail section
        details_lables=clearStringList(response.css('#issuedetails > li > div > strong::text').extract())
         
		#TODO: Extract correct the values of the details section
        details_values=response.css('#issuedetails span.value > span::text').extract() 
        valueList=clearStringList(details_values)
        
        #parsing the people section fields. The first span is always an image for both the Assignee and the Reporter => Select the second element
        peopleDictNew = {'Assignee' : str(response.css('span#assignee-val.view-issue-field > span.user-hover::text').extract()[1]).replace('\n', '').strip(),
                         'Reporter' : str(response.css('span#reporter-val.view-issue-field > span.user-hover::text').extract()[1]).replace('\n', '').strip(),
                         'Votes'    : response.css('#vote-data::text').extract(),
                         'Watchers'	: response.css('#watcher-data::text').extract()
                        }						 
        
        #dates section. Get the list of all the fields in the date section as well as their values
        dates_labels=clearStringList(response.css('div#datesmodule.module > div.mod-content ul li dl.dates dt::text').extract())
        dates_values=response.css('dd.date time.livestamp::text').extract()
        
        #get the epoch format of the date
        epochDates = epochDate(dates_values)
         
        #TODO extract comments section         //*[@class="activity-comment"]/div[1]/div[2]/p/text()
        comments_values=response.css('div#comment-15748543.issue-data-block p::text').extract() 
        print(comments_values)
		#combine all the parsed comments into a single field
        comments_values=" ".join(comments_values)
        
		#extract description section
        descriptionValues=response.css('div.user-content-block p::text').extract()
        #combine all the parsed comments into a single field
        descriptionValues=" ".join(descriptionValues)

		#building the dictionnaries
        #combining the dictionnaries into one global one
        descrDict={'description' : descriptionValues} #key : value
        commentsDict={'comments' : comments_values}
        datesDict= dict(zip(dates_labels, isoTimeFormat(dates_values)))
        datesEpochDict=dict(zip(epochDateLabels(dates_labels),epochDates))
        dicDetailsValue = dict(zip(details_lables, valueList))
        dicDetailsValue.update(datesDict)
        dicDetailsValue.update(datesEpochDict)
        dicDetailsValue.update(peopleDictNew)
        dicDetailsValue.update(commentsDict)
        dicDetailsValue.update(descrDict)
        
        scraped_info = dicDetailsValue

        yield scraped_info