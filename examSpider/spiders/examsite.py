# -*- coding: utf-8 -*-
import scrapy

from examSpider.items import ExamSiteItem, ExamSiteItemLoader

class ExamSiteSpider(scrapy.Spider):
	name = 'examsite'
	allowed_domains = ['www.hao123.com']
	start_urls = ['http://www.hao123.com/exam/wangzhi/']

	def parse(self, response):
		post_nodes = response.css('#bd .mod-content')
		for post_node in post_nodes:
			exam_title = post_node.css('.content-title::text').extract_first("")
			exam_table = {
				'公务员考试':'gongwuyuan',
				'考研':'kaoyan',
				'高考/自/成考':'shengxue',
				'英语类考试':'yingyu',
				'专业类考试':'zhuanye',
				'网校':'wangxiao',
				'分类推广':'fenlei',
			}
			exam_type = exam_table.get(exam_title)
			link_nodes = post_node.css('.content-link .text-con')
			for link_node in link_nodes:
				item_loader = ExamSiteItemLoader(item=ExamSiteItem())
				item_loader.add_value('exam_type', exam_type)
				item_loader.add_value('exam_title', exam_title)
				item_loader.add_value('exam_name', link_node.css('::text').extract_first(""))
				item_loader.add_value('exam_url', link_node.css('::attr(href)').extract_first(""))

				examsite_item = item_loader.load_item()

				yield examsite_item
