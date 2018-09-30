# -*- coding: utf-8 -*-
import scrapy
from panberes_price.items import Product
from panberes_price.settings import PANBERES_USERNAME,PANBERES_PASSWORD
class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['www.panberes.ir']
    start_urls = ['https://www.panberes.ir/Account/Login?ReturnUrl=/Search/Filter']
    def parse(self,response):
        token =  response.css("input[name='__RequestVerificationToken']::attr(value)").extract()
        return [scrapy.http.FormRequest("https://www.panberes.ir/Account/Login",method ="POST",
                    formdata={'Username': PANBERES_USERNAME, 'Pass': PANBERES_PASSWORD,
                    "__RequestVerificationToken":token[0],
                    "__RequestVerificationToken":token[1],
                    'ReturnUrl':"/Search/Filter",
                    "RealPersonCode":"IGVQ",
                    "RealPersonHash":"2089177244"
                    },
                    callback=self.after_login)]

    def after_login(self, response):
        if len(response.css(".usermenu-v1").extract())>0 :
            products = response.css('.product-shop')
            for product in products:
                link = "https://www.panberes.ir"+product.css(".product-item-photo>a::attr(href)").extract_first()
                yield scrapy.http.Request(link, callback=self.parse_product)

            pages = [a for a in response.css('.pagination>li>a::text').extract() if a.isdigit()]
            if len(pages)>1:
                for link in ["https://www.panberes.ir/Search/Filter?page="+page for page in pages]:
                    yield scrapy.http.Request(link, callback=self.after_login)
    
    def parse_product(self,response):
        title = response.css("h1::text").extract_first()
        price = response.css(".shop-product-prices>.shop-purple::text").extract_first()
        count = response.css(".shop-red::text").extract_first()
        try:
            price = int(price.replace("ریال","").replace(",",""))
        except Exception as e:
            price = 0
        try:
            count = int(count)
        except Exception as e:
            count = 0
        yield Product(count=count,price=price,title=title,link=response.url)