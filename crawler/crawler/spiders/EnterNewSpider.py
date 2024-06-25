import scrapy
import time
from ..items import enternewsItem


class EnterNewsSpider(scrapy.Spider):
    name = "enterNews"
    start_urls = ["https://diendandoanhnghiep.vn/dau-tu-chung-khoan-c124"]
    page_num = 2
    
    def parse(self, response):
        all_articles = response.css('li.item.blv2-item')
        for article in all_articles:
            link = article.css('a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(link), callback=self.parse_article)
            
        nextPage = 'https://diendandoanhnghiep.vn/dau-tu-chung-khoan-c124/page-' + str(EnterNewsSpider.page_num) + '.html'
        if EnterNewsSpider.page_num <= 151:
            EnterNewsSpider.page_num += 1
            yield scrapy.Request(nextPage, callback=self.parse)
        
    def parse_article(self, response):
        title = response.css('h1.post-title.main-title::text').extract_first()
        content = response.css('div.post-content p::text').extract()
        if title and content:
            yield{
                'title': title,
                'content': content
            }