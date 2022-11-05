from itemadapter import ItemAdapter
from opensearchpy import OpenSearch


class ArticlePipeline:
    def process_item(self, item, spider):
        return item


class OpenSearchPipeline:

    index_name = "articles"
    index_body = {
        "settings": {"index": {"number_of_shards": 4}},
        "mappings": {
            "properties": {
                "vol": {"type": "integer"},
                "issue": {"type": "integer"},
                "climb_year": {"type": "integer"},
                "publication_year": {"type": "integer"},
            }
        },
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
