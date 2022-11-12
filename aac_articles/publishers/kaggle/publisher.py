import logging
import subprocess

import pandas as pd
from opensearchpy import OpenSearch

logging.basicConfig(
    filename="logs/publishers.log",
    format="%(asctime)s | %(module)s | %(levelname)s:%(message)s",
    encoding="utf-8",
    level=logging.INFO,
)


class KagglePublisher(object):
    def __init__(self, host: str, port: str, auth: tuple):

        self.data_dir = "aac_articles/dataset/kaggle"
        self.data_file = f"articles.csv"
        self.no_publish_cols = ["scraped_at", "referer"]
        self.client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            http_compress=True,  # enables gzip compression for request bodies
            http_auth=auth,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

    def __publish_new_dataset(self):
        return subprocess.run([f"poetry run kaggle datasets create -p {self.data_dir}"], shell=True, check=True)

    @staticmethod
    def __publish_new_dataset_version():
        logging.warning("<publish_new_dataset_version> action not implemented yet!")

    def publish(self, new_version: bool = False):

        scroll_ids = []
        dataset = []

        response = self.client.search(body={"query": {"match_all": {}}}, index="articles", size=1000, scroll="10m")
        logging.info(f"found {response['hits']['total']['value']} articles.")

        scroll_ids.append(response["_scroll_id"])
        dataset.extend([hit["_source"] for hit in response["hits"]["hits"]])

        while response["hits"]["total"]["value"] != len(dataset):

            response = self.client.scroll(scroll_id=response["_scroll_id"], scroll="10m")

            scroll_ids.append(response["_scroll_id"])
            dataset.extend([hit["_source"] for hit in response["hits"]["hits"]])

        self.client.clear_scroll(body={"scroll_id": scroll_ids})

        dataset = pd.DataFrame.from_records(dataset)

        dataset.drop(self.no_publish_cols, axis=1, inplace=True)

        dataset.to_csv(f"{self.data_dir}/{self.data_file}", index=False)

        return self.__publish_new_dataset_version() if new_version else self.__publish_new_dataset()
