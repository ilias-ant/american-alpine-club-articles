from itemloaders.processors import Compose, Join, TakeFirst
from scrapy.loader import ItemLoader

from . import items


class ArticleLoader(ItemLoader):

    default_output_processor = Compose(TakeFirst())
    default_item_class = items.Article

    vol_out = Compose(TakeFirst(), int)
    issue_out = Compose(TakeFirst(), int)
    body_out = Compose(Join(), str.strip)
    author_out = Compose(TakeFirst(), str.strip, lambda x: x.replace(".", "") if x.endswith(".") else x)
    climb_year_out = Compose(TakeFirst(), lambda x: x.replace(".", ""), str.strip, int)
    publication_year_out = climb_year_out
