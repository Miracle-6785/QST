import scrapy
# from scrapy_splash import SplashRequest 
# from scrapy_selenium import SeleniumRequest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
from ..items import VnexpresstrainItem
import time



class VnExpressSpider(scrapy.Spider):
    name = "vnExpress" #crawl name for command
    page_num = 2
    start_urls = ["https://vnexpress.net/kinh-doanh/chung-khoan"]
    
    def parse(self, response):
        all_div_articles = response.css('article.item-news.item-news-common.thumb-left')
        for article in all_div_articles:
            link = article.css('div.thumb-art a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(link), callback=self.parse_article)

        next_page = response.css('a.next-page::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        
    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        
        item = VnexpresstrainItem()
        title = response.css('h1.title-detail::text').extract_first()
        content = response.css('article.fck_detail p::text').extract()
        item['title'] = title
        item['content'] = content
        
        if content:
            yield item