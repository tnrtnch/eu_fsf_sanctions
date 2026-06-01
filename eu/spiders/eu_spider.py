import os
import scrapy
import csv
import io
from eu.items import EuItem


class EuSpider(scrapy.Spider):
    name = "eu_spider"

    custom_settings = {
        "LOG_LEVEL": "INFO",
        "DOWNLOAD_TIMEOUT": 60,
        "ITEM_PIPELINES": {
            "eu.pipelines.EuPipeline": 300,
        },
    }

    TARGET_URL = os.getenv(
        "TARGET_URL",
        "https://data.opensanctions.org/datasets/latest/eu_fsf/targets.simple.csv"
    )

    def start_requests(self):
        self.logger.info(f"TARGET URL: {self.TARGET_URL}")

        yield scrapy.Request(
            url=self.TARGET_URL,
            callback=self.parse_csv,
            dont_filter=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0"
                ),
                "Accept": "text/csv,text/plain,*/*",
            }
        )

    def parse_csv(self, response):
        self.logger.info(f"STATUS: {response.status}")
        self.logger.info(f"RESPONSE LENGTH: {len(response.text)}")

        with open("debug_response.txt", "w", encoding="utf-8") as f:
            f.write(response.text[:10000])

        if response.status != 200:
            raise Exception(
                f"Bad response status: {response.status}"
            )

        reader = csv.DictReader(
            io.StringIO(response.text)
        )

        count = 0

        for row in reader:
            name = row.get("name", "").strip()

            if not name:
                continue

            count += 1

            yield EuItem(
                name=name,
                schema=row.get("schema", "").strip(),
                sanctions=row.get("sanctions", "").strip(),
                aliases=row.get("aliases", "").strip(),
            )

        self.logger.info(f"TOTAL VALID ROWS: {count}")

        if count < 100:
            raise Exception(
                f"Too few rows scraped: {count}"
            )
