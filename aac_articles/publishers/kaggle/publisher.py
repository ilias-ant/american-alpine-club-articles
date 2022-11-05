import subprocess

import pandas as pd
from opensearchpy import OpenSearch


class KagglePublisher(object):
    def __init__(self, host: str, port: str, auth: tuple):

        self.data_dir = "aac_articles/dataset/kaggle"
        self.data_file = f"articles.csv"
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

    def __publish_new_dataset_version(self):
        print("[WARNING]: <publish_new_dataset_version> action not implemented yet!")

    def publish(self, new_version: bool = False):

        scroll_id = None
        dataset = []
        response = self.client.search(body={"query": {"match_all": {}}}, index="articles", scroll="10m")
        dataset.extend([hit["_source"] for hit in response["hits"]["hits"]])

        while "_scroll_id" in response:
            scroll_id = response["_scroll_id"]
            response = self.client.scroll(scroll_id=scroll_id)
            dataset.extend([hit["_source"] for hit in response["hits"]["hits"]])

        self.client.clear_scroll(scroll_id=scroll_id)

        dataset = pd.DataFrame.from_records(dataset)

        dataset.to_csv(f"{self.data_dir}/{self.data_file}", index=False)

        if new_version:
            self.__publish_new_dataset_version()
        else:
            self.__publish_new_dataset()
