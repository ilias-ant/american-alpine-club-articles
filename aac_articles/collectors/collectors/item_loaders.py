import re
from urllib import parse

from itemloaders.processors import Compose, Join, TakeFirst
from scrapy.loader import ItemLoader

from . import items
from .processors import TakeLast

TRAILING_DOT_REGEX = r"\.$"


class ArticleLoader(ItemLoader):

    default_output_processor = Compose(TakeFirst(), str.strip)
    default_item_class = items.Article

    body_out = Compose(Join())
    author_out = Compose(TakeLast(), str.strip, lambda x: re.sub(TRAILING_DOT_REGEX, "", x))
    climb_year_out = Compose(
        lambda years: [y for y in years if "N/A" not in y],
        TakeLast(),
        str.strip,
        lambda x: re.sub(TRAILING_DOT_REGEX, "", x),
    )
    publication_year_out = Compose(
        lambda years: [y for y in years if "N/A" not in y],
        TakeLast(),
        lambda x: x.replace("\n", ""),
        lambda x: x.replace("|", ""),
        str.strip,
        lambda x: re.sub(TRAILING_DOT_REGEX, "", x),
    )
    link_to_pdf_out = Compose(
        TakeFirst(),
        lambda url: parse.urljoin("https://publications.americanalpineclub.org/", url)
        if not url.startswith("http")
        else url,
    )
    referer_out = Compose(TakeFirst(), lambda x: x.decode("utf-8"))
