import scrapy
from ..items import YellowpagesPhParserItem
from scrapy_splash import SplashRequest
from datetime import datetime

class YellowpagesPhParser(scrapy.Spider):
    name = "yellowpages_ph_parser"

    def start_requests(self):
        url = 'https://www.yellow-pages.ph/search/' + str(self.product) +'/page-1'
        yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):
        href = response.xpath('//*[@id="tab0"]/section/div/div/div/div/h2/a/@href').getall()
        for link in href:
            yield response.follow(link, self.parse_company)
        next_page = response.xpath('//ul[@class="pagination"]/li[3]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_company(self, response):
        item = YellowpagesPhParserItem()
        if response.xpath('//h1[@class="h1-tradename"]/text()').get():
            name = response.xpath('//h1[@class="h1-tradename"]/text()').get()
        elif response.xpath('//h2[@class="h2-businessname"]/text()').get():
              name = response.xpath('//h2[@class="h2-businessname"]/text()').get()
        else:
            name = response.xpath('//h1[@class="h1-single-businessname"]/text()').get()
        contacts = response.xpath('//a[@class="biz-link"]/text()').getall()
        description = response.xpath('//div[@class="moreheight"]/p/text()').get()
        date_and_time = datetime.now().strftime('%y-%m-%d')
        item['name'] = name
        item['product'] = str(self.product)
        item['contacts'] = contacts
        item['source'] = 'https://www.yellow-pages.ph'
        item['hs_code'] = self.hs_code
        item['description'] = description
        item['date_and_time'] = date_and_time
        yield item
