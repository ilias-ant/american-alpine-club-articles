import scrapy


class Article(scrapy.Item):

    url = scrapy.Field()
    type = scrapy.Field()
    dataset = scrapy.Field()
    vol = scrapy.Field()
    issue = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    body = scrapy.Field()
    author = scrapy.Field()
    climb_year = scrapy.Field()
    publication_year = scrapy.Field()
