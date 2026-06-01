import scrapy
import csv
import io
import yaml
from eu.items import EuItem


class EuSpider(scrapy.Spider):
    name = "eu_spider"
    custom_settings = {
        "LOG_LEVEL": "INFO",
        "DOWNLOAD_TIMEOUT": 60,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("scraper.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def start_requests(self):
        yield scrapy.Request(
            url=self.config["target_url"],
            callback=self.parse_csv,
            dont_filter=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0 Safari/537.36"
                ),
                "Accept": "text/csv,text/plain,*/*",
            }
        )

    def parse_csv(self, response):
        self.logger.info(f"STATUS: {response.status}")
        self.logger.info(f"CONTENT TYPE: {response.headers.get('Content-Type')}")
        self.logger.info(f"RESPONSE LENGTH: {len(response.text)}")

        with open("debug_response.txt", "w", encoding="utf-8") as f:
            f.write(response.text[:10000])

        if response.status != 200:
            raise Exception(f"Bad response status: {response.status}")

        if len(response.text) < 100:
            raise Exception("Response too small")

        if "html" in response.text.lower():
            raise Exception("HTML returned instead of CSV")

        reader = csv.DictReader(io.StringIO(response.text))

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

