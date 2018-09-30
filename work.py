from scrapy.crawler import CrawlerProcess
from panberes_price.spiders.products  import ProductsSpider
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
def run():
	process.crawl(ProductsSpider)
	process.start()