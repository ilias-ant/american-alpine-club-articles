# american-alpine-club-datasets

Articles from the American Alpine Club's publications: [AAJ](https://publications.americanalpineclub.org/about_the_aaj) 
and [ANAC](https://publications.americanalpineclub.org/about_the_accidents).

<img src="https://github.com/ilias-ant/american-alpine-club-articles/blob/main/static/kaggle-thumbnail-image.jpg" width="90%" text="Free person hiking in snow mountain photo, public domain sport CC0 image | https://www.rawpixel.com/">

The project consists of the following components:

- **collectors**: a [Scrapy](https://scrapy.org/) project that is responsible for scraping articles from [https://publications.americanalpineclub.org/](https://publications.americanalpineclub.org/).
- **publishers**: functionality that is responsible for the publication of the scraped dataset (e.g. Kaggle)
- **dataset**: the raw dataset, in CSV format.

This work has been published as a [Kaggle dataset](https://www.kaggle.com/datasets/iantonopoulos/american-alpine-club-articles).
