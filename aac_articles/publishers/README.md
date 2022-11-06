# publishers

Functionality that is responsible for the publication of the scraped dataset (e.g. in Kaggle).

To upload dataset to [Kaggle](https://www.kaggle.com/), first make sure that: 

1. the [Opensearch](https://opensearch.org/) cluster is up and running.
2. the ``articles`` spider of the ``collectors`` component has completed a full scraping.
3. Kaggle authentication - through API token - is properly configured for [kaggle-api](https://github.com/Kaggle/kaggle-api).  

Then, assuming that you have already set up a Python virtual environment for this project:

```shell
poetry install
```

and at the root directory level type:

```shell
kaggle_publish_new_dataset
```

in order to publish as a new dataset.

If you want to publish a new version of the dataset instead, type:

```shell
kaggle_publish_new_dataset_version
```
