# -*- coding: utf-8 -*-
import scrapy
import time

from examSpider.items import JiaotongItem
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.selector import Selector


# 使用selenium操作chromedriver或phantomjs爬取动态信息
class JiaotongSpider(scrapy.Spider):
	name = 'jiaotong'
	allowed_domains = ['life.hao123.com']
	start_urls = ['http://life.hao123.com/jiaotong/']

	def __init__(self):
		# chromedriver 参考文档https://www.zybuluo.com/mwumli/note/222253
		self.browser = webdriver.Chrome(executable_path="D:/chromedriver.exe")
		# 设置chromedriver不加载图片
		# chrome_opt = webdriver.ChromeOptions()
		# prefs = {"profile.managed_default_content_settings.images":2}
		# chrome_opt.add_experimental_option("prefs", prefs)

		# phantomjs, 无界面的浏览器， 多进程情况下phantomjs性能会下降很严重
		# self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs/bin/phantomjs.exe")
		super(JiaotongSpider, self).__init__()
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_closed(self, spider):
		print('spider closed')
		self.browser.quit()

	def parse(self, response):
		self.browser.get(response.url)
		map_areas = self.browser.find_elements_by_css_selector('.item-map area')
		# print(len(map_areas))
		for map_area in map_areas:
			time.sleep(1)
			map_area.click()
			area_title = map_area.get_attribute('title')
			# print('='*20+area_title)
			s_selector = Selector(text=self.browser.page_source)
			post_nodes = s_selector.css('.sub-areas li.cur')
			# print('-'*20+str(len(post_nodes)))
			for post_node in post_nodes:
				jiaotong_item = JiaotongItem()
				jiaotong_item['city'] = post_node.css('a::text').extract_first('')
				jiaotong_item['area'] = area_title
				yield jiaotong_item