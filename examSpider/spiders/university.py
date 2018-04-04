# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request

from examSpider.items import UniversityItem, UniversityItemLoader

class UniversitySpider(scrapy.Spider):
	name = 'university'
	allowed_domains = ['www.hao123.com']
	start_urls = ['http://www.hao123.com/edu/']

	def parse(self, response):
		post_nodes = response.css('.edu-container tr')
		for post_node in post_nodes:
			uni_address = post_node.css('.first::text').extract_first("")
			uni_address_short = post_node.css('td:nth-child(2) a::attr(href)').extract_first("")
			re_short = re.match('.*?eduhtm/(\w+).htm', uni_address_short)
			if re_short:
				uni_address_short = re_short.group(1).replace('edu', '')
			# print(uni_address, uni_address_short)
			post_links = post_node.css('td a')
			for post_link in post_links:
				list_url = post_link.css('::attr(href)').extract_first("")
				re_url = re.match('.*?eduhtm/.*(\d+).htm', list_url)
				td_index = 0
				type_list = ['normal', 'vocational', 'independent', 'adult']
				if re_url:
					td_index = int(re_url.group(1)) - 1
				# print (td_index, type_list[td_index])
				yield Request(url=list_url, meta={
					'address': uni_address,
					'address_short': uni_address_short,
					'type': type_list[td_index],
				}, callback=self.parse_list)

	def parse_list(self, response):
		address = response.meta.get("address", "")
		address_short = response.meta.get("address_short", "")
		type = response.meta.get("type", "")
		link_nodes = response.css('.bgg table td a')
		for link_node in link_nodes:
			item_loader = UniversityItemLoader(item=UniversityItem(), response=response)
			university = link_node.css('::text').extract_first("")
			url = link_node.css('::attr(href)').extract_first("")
			item_loader.add_value('address', address)
			item_loader.add_value('address_short', address_short)
			item_loader.add_value('university', university)
			item_loader.add_value('type', type)
			item_loader.add_value('url', url)
			university_item = item_loader.load_item()

			yield university_item