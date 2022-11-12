from urllib import parse

import scrapy

from .. import item_loaders


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["publications.americanalpineclub.org"]
    start_urls = ["https://publications.americanalpineclub.org/articles"]

    def parse(self, response, **kwargs):

        last_page = response.xpath('//nav[contains(@class, "pagination")]//input[@type="number"]/@max').get()
        self.logger.info(f"Found {last_page} pages.")

        for page in range(1, int(last_page)):

            params = {"page": page}

            yield scrapy.Request(
                url="https://publications.americanalpineclub.org/articles?" + parse.urlencode(params),
                callback=self.parse_page,
            )

    def parse_page(self, response):

        articles = response.xpath('//div[@class="article"]')

        for article in articles:

            type_ = article.xpath(".//div/span[1]/text()").get()
            publication = article.xpath(".//div/span[2]/text()").get()
            author = article.xpath(".//i/text()").get()
            publication_year = article.xpath(
                './strong[contains(./text(), "Published")]/following-sibling::text()[1]'
            ).get()

            url = article.xpath(".//a/@href").get()

            yield scrapy.Request(
                url=parse.urljoin("https://publications.americanalpineclub.org/", url),
                dont_filter=False,  # visit each article once
                callback=self.parse_article,
                cb_kwargs={
                    "metadata": {
                        "type": type_,
                        "publication": publication,
                        "author": author,
                        "publication_year": publication_year,
                    }
                },
            )

    @staticmethod
    def parse_article(response, metadata):

        article = item_loaders.ArticleLoader(response=response)

        article.add_value("url", response.url)
        article.add_value("referer", response.request.headers.get("Referer"))
        article.add_value("type", metadata["type"])
        article.add_value("publication", metadata["publication"])
        article.add_xpath("title", '//div[contains(@class, "article-body")]//h2[@class="title"]/text()')
        article.add_xpath("location", '//div[contains(@class, "article-body")]//h5/text()')
        article.add_xpath("body", '//div[@id="article"]//descendant::text()')
        article.add_xpath(
            "climb_year",
            '//div[contains(@class, "article-body")]/div/'
            'span[contains(., "Author") and contains(., "Climb Year") and contains(., "Publication Year")]/i[2]/text()',
        )
        article.add_xpath("link_to_pdf", '//a[@title="Download PDF"]/@href')

        article.add_value("author", metadata["author"])
        article.add_xpath("author", '//div[contains(@class, "article-body")]/div/span[contains(., "Author")]/i/text()')
        article.add_xpath(
            "author",
            '//div[contains(@class, "article-body")]/div/'
            'span[contains(., "Author") and contains(., "Climb Year") and contains(., "Publication Year")]/i[1]/text()',
        )

        article.add_value("publication_year", metadata["publication_year"])
        article.add_xpath(
            "publication_year",
            '//div[contains(@class, "article-body")]/div/span[contains(./text(), "Publication Year")]/i/text()',
        )
        article.add_xpath(
            "publication_year",
            '//div[contains(@class, "article-body")]/div/'
            'span[contains(., "Publication Year") and contains(., "Author") and contains(., "Climb Year")]'
            "/i[3]/text()",
        )
        article.add_xpath(
            "publication_year",
            '//div[contains(@class, "article-body")]/div/'
            'span[contains(., "Publication Year") and not(contains(., "Author")) and contains(., "Climb Year")]'
            "/i[2]/text()",
        )

        yield article.load_item()
