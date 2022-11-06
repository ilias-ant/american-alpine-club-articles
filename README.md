# american-alpine-club-datasets

[![Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/iantonopoulos/american-alpine-club-articles)

Articles from the American Alpine Club's publications: [AAJ](https://publications.americanalpineclub.org/about_the_aaj) 
and [ANAC](https://publications.americanalpineclub.org/about_the_accidents). 

This work has been published as a [Kaggle dataset](https://www.kaggle.com/datasets/iantonopoulos/american-alpine-club-articles).

<img src="https://github.com/ilias-ant/american-alpine-club-articles/blob/main/static/kaggle-thumbnail-image.jpg" width="90%" text="Free person hiking in snow mountain photo, public domain sport CC0 image | https://www.rawpixel.com/">

The project consists of the following components:

- **collectors**: a [Scrapy](https://scrapy.org/) project, responsible for scraping articles from [https://publications.americanalpineclub.org](https://publications.americanalpineclub.org/).
- **opensearch-cluster**: an [OpenSearch](https://opensearch.org/) cluster, where the scraped articles are indexed.
- **publishers**: functionality responsible for the publication of the articles index (e.g. as Kaggle dataset).
- **dataset**: the raw dataset, in CSV format.
