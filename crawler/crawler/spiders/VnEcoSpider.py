import scrapy
# from scrapy_splash import SplashRequest 
# from scrapy_selenium import SeleniumRequest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
from ..items import VnEconomyItem

class VnEcoSpider(scrapy.Spider):
    name = "vnEco"
    start_urls = ['https://vneconomy.vn/chung-khoan.htm']
    page_num = 2
    

    def parse(self, response):
        all_div_articles = response.css('article.story.story--featured.story--timeline')
        for article in all_div_articles:
            link = article.css('a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(link), callback=self.parse_article)
        
        next_page = 'https://vneconomy.vn/chung-khoan.htm?trang=' + str(VnEcoSpider.page_num)
        if VnEcoSpider.page_num <= 301: # 300 pages crawled
            VnEcoSpider.page_num += 1
            yield scrapy.Request(next_page, callback=self.parse)
        
    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        
        item = VnEconomyItem()
        title = response.css('h1.detail__title::text').extract_first()
        content = response.css('div.detail__content p::text').extract()
        
        item['title'] = title
        item['content'] = content
        if title and content:
            yield item