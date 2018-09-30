import sys
import psycopg2
import hashlib,datetime,codecs
from scrapy.exceptions import DropItem
from scrapy.http import Request
from .settings import DB
class StorePipeline(object):
	def process_item(self, item, spider):
		conn = psycopg2.connect(**DB)
		cursor = conn.cursor()
		try:
			q = """INSERT INTO products (title, price,link , count , updated_at) VALUES 
			('{}', {},'{}',{},'{}') ON CONFLICT (title) do update set updated_at = Excluded.updated_at,count =Excluded.count,price = Excluded.price  """.format(item['title'], item['price'], item['link'],
				item['count'],str(datetime.datetime.now()).split('.')[0])
			cursor.execute(q)
			conn.commit()
		except Exception as e:
			print(e)
		conn.close()
		return item