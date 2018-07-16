# -*- coding: utf-8 -*-
import re
import scrapy
from crawl.items import CrawlItem
class WySpider(scrapy.Spider):
    name="wycrawl"
    allowed_domains=["51job.com"]
    start_urls=["https://search.51job.com/list/000000,000000,0000,03,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="]

    def parse(self,response):
        url=response.xpath('//*[@class="bk"]/*/@href').extract()
        print('******************************************************')
        print('******************************************************')
        print('******************************************************')
        if len(url)==1:
            url=url[0]
        else:
            url=url[1]
        yield scrapy.Request(url,callback=self.parse)
        
        for href in response.xpath('//*[@id="resultList"]/div/p/span/a/@href').extract():
            if href!=None:
                try:
                    
                    yield scrapy.Request(href,callback=self.parse_item)
                except:
                    continue
        
                
    def parse_item(self, response):
        try:  
            item = CrawlItem()
            item['url']=response.url
            time = response.xpath("//*[@class='t1']//*/text()").extract()[0]
            time=re.sub('\r|\n|\t|　|\xa0| ', '', time)
            item['time']=time
            info = ''.join(response.xpath("//*[@class='bmsg job_msg inbox']//*/text()").extract())
            info=re.sub('\r|\n|\t|　|\xa0| ', '',info)
            item['info']=info
            company = response.xpath("//*[@class='cname']/a/@title").extract()[0]
            company=re.sub('\r|\n|\t|　|\xa0| ', '',company)
            item['company']=company
            ctype = response.xpath("//*[@class='msg ltype']/text()").extract()[0]
            ctype=re.sub('\r|\n|\t|　|\xa0| ', '',ctype)
            item['ctype']=ctype
            return item
        except:
            pass