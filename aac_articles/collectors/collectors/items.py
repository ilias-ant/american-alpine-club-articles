import scrapy


class TimestampedItem(scrapy.Item):

    scraped_at = scrapy.Field()


class Article(TimestampedItem):

    url = scrapy.Field()
    type = scrapy.Field()
    publication = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    body = scrapy.Field()
    author = scrapy.Field()
    climb_year = scrapy.Field()
    publication_year = scrapy.Field()
    link_to_pdf = scrapy.Field()
    referer = scrapy.Field()
