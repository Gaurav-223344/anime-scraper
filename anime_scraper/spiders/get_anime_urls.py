import os
from typing import List
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json


class GetAnimeUrlsSpider(scrapy.Spider):
    name = "get_anime_urls"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    data_dir = os.path.join("data")
    custom_settings = {
        "FEEDS": {
            os.path.join(data_dir, "anime_urls.json"): {
                "format": "json",
                "encoding": "utf-8",
                "overwrite": True,
            },
        },
        "LOG_FILE": os.path.join(data_dir, "anime_urls.log"),
    }

    def __init__(self, file, *args, **kwargs):
        super(GetAnimeUrlsSpider, self).__init__(*args, **kwargs)
        self.file = file

    def start_requests(self):
        with open(self.file, "r", encoding="utf-8") as json_data:
            page_urls_json: List[dict] = json.load(json_data)

        for page_urls_dict in page_urls_json:
            anime_url = page_urls_dict.get("page_url")
            yield scrapy.Request(url=anime_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        # file = os.path.join("data", "index.html")
        # html = ""
        # with open(file, "r", encoding="utf-8") as html_file:
        #     # html_file.write(response.text)
        #     for line in html_file.read():
        #         html += line

        # response = Selector(text=html)

        table_rows = response.css("div.js-categories-seasonal").css("table").css("tr")
        if table_rows and len(table_rows) > 1:
            for table_row in table_rows[1:]:
                title = table_row.css("div.title a strong::text").get()
                url = table_row.css("div.title a::attr('href')").get()
                yield {"title": title, "url": url}

        # print(response.css("div.js-categories-seasonal").css("div.ac").css("a")[-1].css("a::text").get())


if __name__ == "__main__":
    pages_urls_file = os.path.join("data", "pages_urls.json")
    # process = GetAnimeUrlsSpider(pages_urls_file)
    # process.parse("")

    process = CrawlerProcess()
    process.crawl(GetAnimeUrlsSpider, pages_urls_file)
    process.start()
