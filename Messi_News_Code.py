import scrapy
import datetime


class GoalSpider(scrapy.Spider):
    name = 'goal'
    
    def start_requests(self):
        urls = []
        urls.append("https://www.goal.com/en/player/lionel-messi/1/c5ryhn04g9goikd0blmh83aol")
        for i in range(2,5000):
            urls.append("https://www.goal.com/en/player/lionel-messi/"+str(i)+"/c5ryhn04g9goikd0blmh83aol")
        for url in urls:
            yield scrapy.Request(url= url, callback= self.extract_messi_urls, dont_filter=True)

    def extract_messi_urls(self, response): 
        links = response.xpath('//article[@itemprop = "itemListElement"]/a/@href').extract()
        for i in range(len(links)):
            links[i] = 'https://www.goal.com'+ links[i]
        links = list(set(links))
 
        for link in links:    
            yield scrapy.Request(url=link, callback=self.extract_messi_info, dont_filter=True)
        
    def extract_messi_info(self, response):
        date = response.xpath('//span/time[@class="time"]/text()').extract_first()
        date_format = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%d/%m/%Y')
        if date_format[-4:]>'2017':
            yield {
                'url': response.url,
                'date': date,
                'title':response.xpath('//h1[@class="article_title__Kfsaf"]/text()').extract_first(),
                'summary': response.xpath('//div[@class="article_teaser__1OofW"]/text()').extract_first(),
                'text': ' '.join(response.xpath('//div[@class="body_body__1x16o cms_cms__3hYjB"]/p/text()').getall()),     
            }
        
        # next_page = response.xpath('//a[@class="btn btn--older needsclick"]/@href').get()
        # if next_page is not None:
        #     # if not final_date > date[-1]:
        #     yield response.follow(url= next_page, callback= self.extract_messi_info)
    