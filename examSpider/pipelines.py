# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors

from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline

class MysqlPipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect('127.0.0.1', 'root', '', 'exam', charset='utf8mb4', use_unicode=True)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		insert_sql = """
			insert into universities(address, address_short, university, type, url) values (%s, %s, %s, %s, %s)
		"""
		self.cursor.execute(insert_sql, (self['address'], self['address_short'], self['university'], self['type'], self['url']))
		self.conn.commit()
		return item
		

class MysqlTwistedPipeline(object):
	def __init__(self, dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls, settings):
		dbparms = dict(
			host = settings['MYSQL_HOST'],
			db = settings['MYSQL_DBNAME'],
			user = settings['MYSQL_USER'],
			password = settings['MYSQL_PASSWORD'],
			charset = 'utf8mb4',
			use_unicode = True,
			cursorclass = MySQLdb.cursors.DictCursor,
		)
		dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
		return cls(dbpool)

	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self.do_insert, item)
		query.addErrback(self.handle_error, item, spider)
		return item

	def handle_error(self, failure, item, spider):
		# print(failure)
		pass

	def do_insert(self, cursor, item):
		insert_sql, params = item.get_insert_sql()
		cursor.execute(insert_sql, params)


class ArticleImagePipeline(ImagesPipeline):
	# 修改图片存储路径
	# def file_path(self, request, response=None, info=None):  
	# 	image_name = request.meta['item']['cover_img']
	# 	print('*'*100)
	# 	print(image_name)
	# 	path = 'cover/'+image_name+'/'+request.url[-4:].strip('/')+'.jpg'  
	# 	return path
	        # path = 'full/'+image_name+'/'+request.url[-4:].strip('/')+'.jpg'  
	        # return path

	def item_completed(self, results, item, info):
		for ok, value in results:
			item['cover_img'] = value['path']
		return item