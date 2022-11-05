import re
from urllib import parse

from itemloaders.processors import Compose, Join, TakeFirst
from scrapy.loader import ItemLoader

from . import items


class ArticleLoader(ItemLoader):

    default_output_processor = Compose(TakeFirst())
    default_item_class = items.Article

    body_out = Compose(Join(), str.strip)
    author_out = Compose(TakeFirst(), str.strip, str.strip, lambda x: re.sub(r".$", "", x))
    climb_year_out = Compose(
        lambda years: [y for y in years if "N/A" not in y],
        TakeFirst(),
        str.strip,
        lambda x: re.sub(r".$", "", x),
    )
    publication_year_out = Compose(
        lambda years: [y for y in years if "N/A" not in y],
        TakeFirst(),
        lambda x: x.replace("\n", ""),
        lambda x: x.replace("|", ""),
        str.strip,
        lambda x: re.sub(r".$", "", x),
    )
    link_to_pdf_out = Compose(
        TakeFirst(),
        lambda url: parse.urljoin("https://publications.americanalpineclub.org/", url)
        if not url.startswith("http")
        else url,
    )
