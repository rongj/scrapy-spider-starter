# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class UniversityItemLoader(ItemLoader):
	default_output_processor = TakeFirst()

class UniversityItem(scrapy.Item):
	address = scrapy.Field()
	address_short = scrapy.Field()
	university = scrapy.Field()
	url = scrapy.Field()
	type = scrapy.Field()

	def get_insert_sql(self):
		insert_sql = """
			insert into universities(address, address_short, university, type, url) values (%s, %s, %s, %s, %s)
		"""
		params = (
			self['address'], self['address_short'], self['university'], self['type'], self['url'], 
		)
		return insert_sql, params