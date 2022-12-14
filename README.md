<div align="center">
    <h1>american-alpine-club-datasets</h1>
    <p><a href="https://publications.americanalpineclub.org/">AAC</a>: climbing accidents and major new climbs.</p>
    <a href="https://www.kaggle.com/datasets/iantonopoulos/american-alpine-club-articles">
        <img src="https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white" alt="kaggle dataset">
    </a>
    
</div>
<hr>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Articles from the American Alpine Club's publications: [AAJ](https://publications.americanalpineclub.org/about_the_aaj) 
and [ANAC](https://publications.americanalpineclub.org/about_the_accidents). 

This work has been published as a [Kaggle dataset](https://www.kaggle.com/datasets/iantonopoulos/american-alpine-club-articles).

<img src="https://github.com/ilias-ant/american-alpine-club-articles/blob/main/static/kaggle-thumbnail-image.jpg" width="90%" text="Free person hiking in snow mountain photo, public domain sport CC0 image | https://www.rawpixel.com/">

The project consists of the following components:

- **collectors**: a [Scrapy](https://scrapy.org/) project, responsible for scraping articles from [publications.americanalpineclub.org](https://publications.americanalpineclub.org/).
- **opensearch-cluster**: an [OpenSearch](https://opensearch.org/) cluster, where the scraped articles are indexed.
- **publishers**: functionality responsible for the publication of the articles index (e.g. as Kaggle dataset).
- **notebooks**: a collection of Jupyter notebooks, for various dataset-based explorations and applications.
- **dataset**: the raw dataset, in CSV format.

## Citation

```bibtex
@misc{ilias antonopoulos_2022, 
      title={AAC: climbing accidents and major new climbs}, 
      url={https://www.kaggle.com/dsv/4457812}, 
      DOI={10.34740/KAGGLE/DSV/4457812}, 
      publisher={Kaggle}, 
      author={Ilias Antonopoulos},
      year={2022} 
}
```
