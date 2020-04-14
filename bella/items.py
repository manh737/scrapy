# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BellaItem(scrapy.Item):
    title = scrapy.Field()
    sapo = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()
    tag = scrapy.Field()
    public_date = scrapy.Field()
    image = scrapy.Field()
