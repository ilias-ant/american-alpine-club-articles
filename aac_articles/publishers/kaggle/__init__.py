import os

from .publisher import KagglePublisher


def publish_new_dataset():

    host = os.getenv("OPENSEARCH_HOST", "localhost")
    port = os.getenv("OPENSEARCH_PORT", 9200)
    username = os.getenv("OPENSEARCH_USERNAME", "admin")
    password = os.getenv("OPENSEARCH_PASSWORD", "admin")

    kaggle = KagglePublisher(host=host, port=port, auth=(username, password))
    kaggle.publish(new_version=False)


def publish_new_dataset_version():

    host = os.getenv("OPENSEARCH_HOST", "localhost")
    port = os.getenv("OPENSEARCH_PORT", 9200)
    username = os.getenv("OPENSEARCH_USERNAME", "admin")
    password = os.getenv("OPENSEARCH_PASSWORD", "admin")

    kaggle = KagglePublisher(host=host, port=port, auth=(username, password))
    kaggle.publish(new_version=True)
