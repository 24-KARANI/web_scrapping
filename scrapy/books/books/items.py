
import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    pass
