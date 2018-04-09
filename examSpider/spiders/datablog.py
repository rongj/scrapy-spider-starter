# -*- coding: utf-8 -*-
import scrapy
import time

from examSpider.items import DatablogItem
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.selector import Selector
from scrapy.http import Request

# 爬取网易数读多个tab下的滚动列表数据
class DataBlogSpider(scrapy.Spider):
	name = 'datablog'
	allowed_domains = ['data.163.com']
	start_urls = ['http://data.163.com/special/datablog/']

	def __init__(self):
		# chromedriver 参考文档https://www.zybuluo.com/mwumli/note/222253
		self.browser = webdriver.Chrome(executable_path="D:/chromedriver.exe")
		# 设置chromedriver不加载图片
		chrome_opt = webdriver.ChromeOptions()
		prefs = {"profile.managed_default_content_settings.images":2}
		chrome_opt.add_experimental_option("prefs", prefs)

		# phantomjs, 无界面的浏览器， 多进程情况下phantomjs性能会下降很严重
		# self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs/bin/phantomjs.exe")
		super(DataBlogSpider, self).__init__()
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_closed(self, spider):
		print('spider closed')
		self.browser.quit()

	def parse(self, response):
		self.browser.get(response.url)
		datatabs = self.browser.find_elements_by_css_selector('.blog-top .blog-nav li:not([cate="qb"])')
		print(len(datatabs))
		for datatab in datatabs:
			self.click_tab(datatab)
			# datatab.click()
			# cate_name = datatab.find_element_by_tag_name('h4').text
			# cate = datatab.find_element_by_tag_name('h5').text.lower()
			# s_selector = Selector(text=self.browser.page_source)
			# post_nodes = s_selector.css('.post-list li')
			# print(len(post_nodes))
			# for post_node in post_nodes:
			# 	detail_link = post_node.css('a::attr(href)').extract_first('')
			# 	cover_img = post_node.css('img::attr(src)').extract_first('')
			# 	yield Request(url=detail_link, meta={'cover_img': cover_img, 'cate_name': cate_name, 'cate': cate}, callback=self.parse_detail)

	def click_tab(self, datatab):
		datatab.click()
		cate_name = datatab.find_element_by_tag_name('h4').text
		cate = datatab.find_element_by_tag_name('h5').text.lower()
		s_selector = Selector(text=self.browser.page_source)
		post_nodes = s_selector.css('.post-list li')
		print(len(post_nodes))
		for post_node in post_nodes:
			detail_link = post_node.css('a::attr(href)').extract_first('')
			cover_img = post_node.css('img::attr(src)').extract_first('')
			yield Request(url=detail_link, meta={'cover_img': cover_img, 'cate_name': cate_name, 'cate': cate}, callback=self.parse_detail)

			# time.sleep(1)
			# yield datatab.click()


	def parse_detail(self, response):
		cover_img = response.meta.get('cover_img', '')
		cate_name = response.meta.get('cate_name', '')
		cate = response.meta.get('cate', '')

		datablog_item = DatablogItem()
		datablog_item['title'] = response.css('.main-a .left h1::text').extract_first('')
		datablog_item['content'] = ''.join(response.css('.main-a .left #endText p').extract())
		datablog_item['create_time'] = response.css('.main-a .left #ptime::text').extract_first('')
		datablog_item['cover_img'] = [cover_img]
		datablog_item['cate_name'] = cate_name
		datablog_item['cate'] = cate
		yield datablog_item