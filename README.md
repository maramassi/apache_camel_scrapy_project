# apache_camel_scrapy_project
This project is a Scapry spider that crawls and parses an issue report of the Apache Camel project.

The crawled URL is 
https://issues.apache.org/jira/browse/CAMEL-10597

The used tool is Scrapy 1.6

Through the cmd, run the following command to run the spider, crawl the requested page and insert the parsed data in a csv file

scrapy crawl ApacheCamelSpider -o CAMEL-10597.csv -t csv
