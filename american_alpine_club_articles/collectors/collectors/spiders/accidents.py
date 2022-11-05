import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from .. import item_loaders


class AccidentsSpider(scrapy.Spider):
    name = "accidents"
    allowed_domains = ["publications.americanalpineclub.org"]
    start_urls = ["https://publications.americanalpineclub.org/"]

    def __init__(self, year=None, *args, **kwargs):
        super(AccidentsSpider, self).__init__(*args, **kwargs)

        self.year = year

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--kiosk")
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=options)
        self.driver.implicitly_wait(5)

    def parse(self, response):

        self.driver.get(response.url)

        # click "Accidents" (to select)
        accidents = self.driver.find_element(
            By.XPATH, '//form[@action="/articles/search"]//input[@name="search[anac]"]'
        )
        accidents.click()

        # click "AAJ" (to un-select)
        aaj = self.driver.find_element(
            By.XPATH, '//form[@action="/articles/search"]//input[@name="search[publication]"]'
        )
        aaj.click()

        # show advanced search options
        advanced_options = self.driver.find_element(
            By.XPATH, '//a[@aria-controls="advanced-options" and @role="button"]'
        )
        advanced_options.click()

        # select publication year
        year = self.driver.find_element(By.XPATH, '//div[@class="advanced-input"]//input[@name="search[year]"]')
        year.send_keys(self.year)

        search = self.driver.find_element(By.XPATH, '//input[@type="submit" and @value="Search"]')
        search.click()

        self.logger.info(f"Searching for accident articles, with publication year: {self.year}.")

        articles = self.driver.find_elements(
            By.XPATH, '//div[@class="article-list"]/div[contains(@class, "article card")]'
        )

        for article in articles:

            article_type = article.find_element(By.XPATH, './div[contains(@class, "article-type")]/span[1]').text
            dataset = article.find_element(By.XPATH, '//div[contains(@class, "article-type")]/span[2]').text
            vol = article.find_element(By.XPATH, './/p[contains(@class, "details-vol")]/i').text
            issue = article.find_element(By.XPATH, './/p[contains(@class, "details-issue")]/i').text

            url = article.find_element(By.XPATH, 'div[@class="article-title"]/a').get_attribute("href")

            yield scrapy.Request(
                url,
                dont_filter=False,  # visit each article once
                callback=self.parse_article,
                cb_kwargs={
                    "metadata": {
                        "article_type": article_type,
                        "dataset": dataset,
                        "vol": vol,
                        "issue": issue,
                    }
                },
            )

    def parse_article(self, response, metadata):
        self.logger.info(f"Scraping article <{response.url}>.")
        article = item_loaders.ArticleLoader(response=response)

        article.add_value("url", response.url)
        article.add_value("type", metadata["article_type"])
        article.add_value("dataset", metadata["dataset"])
        article.add_value("vol", metadata["vol"])
        article.add_value("issue", metadata["issue"])
        article.add_xpath("title", '//div[contains(@class, "article-body")]//h2[@class="title"]/text()')
        article.add_xpath("location", '//div[contains(@class, "article-body")]//h5/text()')
        article.add_xpath("body", '//div[@id="article"]//descendant::text()')
        article.add_xpath("author", '//div[contains(@class, "article-body")]/div/span/i[1]/text()')
        article.add_xpath("climb_year", '//div[contains(@class, "article-body")]/div/span/i[2]/text()')
        article.add_xpath("publication_year", '//div[contains(@class, "article-body")]/div/span/i[3]/text()')

        yield article.load_item()
