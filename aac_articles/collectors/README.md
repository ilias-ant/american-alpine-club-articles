# collectors

A [Scrapy](https://scrapy.org/) project that is responsible for scraping articles 
from [https://publications.americanalpineclub.org/](https://publications.americanalpineclub.org/).

To scrape all articles from said domain, first initiate an [Opensearch](https://opensearch.org/) cluster via:

```shell
docker compose up
```

To verify that the cluster is healthy:

```shell
curl -XGET --insecure -u 'admin:admin' 'https://localhost:9200/_cluster/health'
```

you should see something like this:

```json
{
  "cluster_name":"opensearch-cluster",
  "status":"green",
  "number_of_nodes":2,
  "number_of_data_nodes":2,
  "discovered_master":true,
  "discovered_cluster_manager":true,
  "active_primary_shards":8,
  ...,
  "active_shards_percent_as_number":100.0
}
```

Then, assuming that you have already set up a Python virtual environment for this project:

```shell
cd aac_articles/collectors
```

and simply:

```shell
scrapy crawl articles
```

The spider ``articles`` will then proceed to scrape each available article from each available page, storing it into
an Opensearch ``articles`` index.

**This might take a while**, because the spider is configured is such a way in order for the domain to be scraped in a 
"gentle" manner, without affecting its performance.

While you're waiting, you may find it useful to:

1. navigate to [http://localhost:5601](http://localhost:5601) for OpenSearch Dashboards.
2. login with the default username (admin) and password (admin).
3. create an index pattern for the ``articles`` index (based on ``scraped_at``).
4. navigate to [http://localhost:5601/app/discover](http://localhost:5601/app/discover/).

and you'll be able to monitor the index live, like so:

<img src="https://github.com/ilias-ant/american-alpine-club-articles/blob/main/static/opensearch-dasboard.png" width="90%">
