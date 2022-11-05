# collectors

A [Scrapy](https://scrapy.org/) project that is responsible for scraping articles 
from [https://publications.americanalpineclub.org/](https://publications.americanalpineclub.org/).

To scrape all articles from said domain, first initiate an [Opensearch](https://opensearch.org/) cluster via:

```shell
docker compose up
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

