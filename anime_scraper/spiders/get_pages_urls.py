import os

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector


class GetPagesUrlsSpider(scrapy.Spider):
    name = "get_pages_urls"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    base_url = "https://myanimelist.net"
    data_dir = os.path.join("data")
    custom_settings = {
        'FEEDS': {
            os.path.join(data_dir, 'pages_urls.json'): {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
            },
        },
        'LOG_FILE': os.path.join(data_dir, 'anime_urls.log')
    }

    def start_requests(self):
        letters = ".ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for letter in letters:
            next_url = self.base_url + "/anime.php?letter=" + str(letter)
            # break
        # print("next_url: ", next_url)
            yield scrapy.Request(url=next_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        # file = os.path.join("data", "index.html")
        # html = ""
        # with open(file, "w", encoding="utf-8") as html_file:
        #     html_file.write(response.text)
        # for line in html_file.read():
        #     html += line

        # response = Selector(text=html)

        number_of_pages = (
            response.css("div.js-categories-seasonal")
            .css("div.ac")
            .css("a")[-1]
            .css("a::text")
            .get()
        )

        # page_urls = []
        for page in range(int(number_of_pages)):
            # page_urls.append()

            yield {"page_url": response.url + f"&show={page * 50}"}


if __name__ == "__main__":
    # process = GetPagesUrlsSpider()
    # process.start_requests()
    # print(process.page_urls)

    process = CrawlerProcess()
    process.crawl(GetPagesUrlsSpider)
    process.start()
