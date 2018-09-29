# -*- coding: utf-8 -*-
import scrapy
from panberes_price.items import Product

class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['www.panberes.ir']
    start_urls = ['https://www.panberes.ir/Search/Filter?page=1/']

    def parse(self, response):
        products = response.css('.product-shop')
        for product in products:
            title = product.css(".product-description p::text").extract()[0]
            price =product.css(".title-price::text").extract()[0].replace("ریال","").replace(",","")
            try:
            	price = int(price)
            except Exception as e:
            	price = 0
            available = len(product.css(".btn.btn-cart").extract()) >0
            yield Product(available=available,price=price,title=title)
        pages = [a for a in response.css('.pagination>li>a::text').extract() if a.isdigit()]
        if len(pages)>1:
            for link in ["https://www.panberes.ir/Search/Filter?page="+page for page in pages]:
                yield scrapy.Request(link, callback=self.parse)
    