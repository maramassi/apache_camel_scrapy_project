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
            newDetail=details.replace(':', '').replace('\n', '').replace('\r', '').replace(' ','')
            newClearedList.append(newDetail)
           return newClearedList
		  
        details_values=[]
		#details_values=response.xpath('#issuedetails span.value:not(img)::text, span.value span a::text, span.value span::text, ul.property-list > li > div > div> div > span::text, ul.property-list > li > div > div::text').extract() 
        detailsItems =response.xpath("//ul[@id='issuedetails']/li[starts-with(@class, 'item')]") #extracting all the li-details items
        details_lables=clearStringList(detailsItems.xpath("//div[@class='wrap']/strong/text()").extract())
        for label in details_lables:
           if label == "FixVersion/s":
             details_lables.remove(label)
        
		#item in detailsItems:
        #details_values.append(item.xpath('/div[@class="wrap"]/span[@class="value"]/text()[not(normalize-space(.)="")]').extract_first());		
        #details_values=clearStringList(detailsItems.xpath('//div[@class="wrap"]/span/text()[not(normalize-space(.)="")] | //div[@class="wrap"]/span[@class="value"]/span/text()[not(normalize-space(.)="")]').extract())# | //div[@class="wrap"]/span[@id="resolution-val"]/text() | //div[@class="wrap"]/span[@class="value"]/span/a/text() | //div[@class="wrap"]/span[@class="value"]/span/span/text() | //div[@class="wrap"]/span[@class="value"]/span/text()').extract())
        details_values=clearStringList(response.css('#issuedetails span.value:not(img)::text, span.value span#components-field a::text, span.value span::text, ul.property-list > li > div > div> div > span::text, ul.property-list > li > div > div::text').extract())# , ul.property-list > li > div > div >span ::text').extract())
        
        while '' in details_values:
           details_values.remove('')
        print(details_values)     

        while ',' in details_values:
           details_values.remove(',')
        print(details_values)     

		#parsing the people section fields. The first span is always an image for both the Assignee and the Reporter => Select the second element
        peopleDictNew = {'Assignee' : str(response.css('span#assignee-val.view-issue-field > span.user-hover::text').extract()[1]).replace('\n', '').strip(),
                         'Reporter' : str(response.css('span#reporter-val.view-issue-field > span.user-hover::text').extract()[1]).replace('\n', '').strip(),
                         'Votes'    : response.css('#vote-data::text').extract(),
                         'Watchers'	: response.css('#watcher-data::text').extract()
                        }						 
        
        #dates section. Get the list of all the fields in the date section as well as their values
        dates_labels=clearStringList(response.css('div#datesmodule.module > div.mod-content ul li dl.dates dt::text').extract())
        dates_values=response.css('dd.date time.livestamp::attr(datetime)').extract()
		#get the epoch format of the date
        epochDates = epochDate(dates_values)
         
        #TODO extract comments section //*[@class="activity-comment"]/div[1]/div[2]/p/text()
        comments_values=response.css('div#comment-15748543.issue-data-block p::text').extract()
        cmt_val= response.css('div.activity-comment div.action-details ::text').extract()		
        print('***********CMT***************')
        print(cmt_val)
        #combine all the parsed comments into a single field
        comments_values=" ".join(comments_values)
        
        #extract description section
        descriptionValues=response.css('div.user-content-block p::text').extract()
        #combine all the parsed comments into a single field
        descriptionValues=" ".join(descriptionValues)

		#building the dictionnaries
        #combining the dictionnaries into a global one
        descrDict={'description' : descriptionValues} #key : value
        commentsDict={'comments' : comments_values}
        datesDict= dict(zip(dates_labels, dates_values))
        datesEpochDict=dict(zip(epochDateLabels(dates_labels),epochDates))
        dicDetailsValue = dict(zip(details_lables, details_values))
        dicDetailsValue.update(datesDict)
        dicDetailsValue.update(datesEpochDict)
        dicDetailsValue.update(peopleDictNew)
        dicDetailsValue.update(commentsDict)
        dicDetailsValue.update(descrDict)
        
        scraped_info = dicDetailsValue

        yield scraped_info