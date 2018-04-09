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


class ExamSiteItemLoader(ItemLoader):
	default_output_processor = TakeFirst()

class ExamSiteItem(scrapy.Item):
	exam_type = scrapy.Field()
	exam_title = scrapy.Field()
	exam_name = scrapy.Field()
	exam_url = scrapy.Field()

	def get_insert_sql(self):
		insert_sql = """
			insert into examsites(exam_type, exam_title, exam_name, exam_url) values (%s, %s, %s, %s)
		"""
		params = (
			self['exam_type'], self['exam_title'], self['exam_name'], self['exam_url'],
		)
		return insert_sql, params


class JiaotongItem(scrapy.Item):
	city = scrapy.Field()
	area = scrapy.Field()

	def get_insert_sql(self):
		insert_sql = """
			insert into areas(city, area) values (%s, %s)
		"""
		params = (
			self['city'], self['area'],
		)
		return insert_sql, params


class DatablogItem(scrapy.Item):
	title = scrapy.Field()
	content = scrapy.Field()
	cover_img = scrapy.Field()
	cate_name = scrapy.Field()
	cate = scrapy.Field()
	create_time = scrapy.Field()

	def get_insert_sql(self):
		insert_sql = """
			insert into datablogs(title, content, cover_img, cate_name, cate, create_time) values (%s, %s, %s, %s, %s, %s)
		"""
		params = (
			self['title'], self['content'], self['cover_img'], self['cate_name'], self['cate'], self['create_time'],
		)
		return insert_sql, params