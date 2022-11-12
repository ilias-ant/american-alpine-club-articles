from datetime import datetime

from itemadapter import ItemAdapter
from opensearchpy import OpenSearch
from scrapy import exceptions


class ArticlePipeline:
    def process_item(self, item, spider):

        expectations = (
            item["publication"] in ("ANAM", "AAJ"),
            ("publication_year" in item) and (len(item["publication_year"]) == 4),
        )

        if not all(expectations):
            raise exceptions.DropItem()

        item["scraped_at"] = datetime.utcnow().isoformat()  # in ISO 8601 format

        return item


class OpenSearchPipeline:

    index_name = "articles"
    index_body = {
        "settings": {"index": {"number_of_shards": 4}},
    }

    def __init__(self, host: str, port: int, auth: tuple):
        self.client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            http_compress=True,  # enables gzip compression for request bodies
            http_auth=auth,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings["OPENSEARCH_HOST"],
            port=crawler.settings["OPENSEARCH_PORT"],
            auth=(crawler.settings["OPENSEARCH_USERNAME"], crawler.settings["OPENSEARCH_PASSWORD"]),
        )

    def open_spider(self, spider):

        if self.client.indices.exists(index=self.index_name):
            return

        self.client.indices.create(self.index_name, body=self.index_body)

    def process_item(self, item, spider):

        document = ItemAdapter(item).asdict()

        self.client.index(
            index=self.index_name,
            body=document,
            id=document["url"],
            refresh=True,
        )

        return item

    def close_spider(self, spider):
        self.client.close()
