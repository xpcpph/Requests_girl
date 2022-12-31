# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 在这里为项目定义字段
    title_name = scrapy.Field()
    secondary_url = scrapy.Field()
