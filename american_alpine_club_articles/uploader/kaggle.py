import json
import os
import subprocess

from opensearchpy import OpenSearch


def upload_to_kaggle():

    host = os.getenv("OPENSEARCH_HOST", "localhost")
    port = os.getenv("OPENSEARCH_PORT", 9200)
    username = os.getenv("OPENSEARCH_USERNAME", "admin")
    password = os.getenv("OPENSEARCH_PASSWORD", "admin")

    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_compress=True,  # enables gzip compression for request bodies
        http_auth=(username, password),
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )

    scroll_id = None
    dataset = []
    response = client.search(body={"query": {"match_all": {}}}, index="articles", scroll="10m")
    dataset.extend([hit["_source"] for hit in response["hits"]["hits"]])

    while "_scroll_id" in response:

        scroll_id = response["_scroll_id"]
        response = client.scroll(scroll_id=scroll_id)
        dataset.extend([hit["_source"] for hit in response["hits"]["hits"]])

    client.clear_scroll(scroll_id=scroll_id)

    json_object = json.dumps(dataset, indent=4)

    with open("american_alpine_club_articles/raw/sample.json", "w") as outfile:
        outfile.write(json_object)

    subprocess.run(["poetry run kaggle datasets create -p american_alpine_club_articles/raw"], shell=True, check=True)


if __name__ == "__main__":

    upload_to_kaggle()
