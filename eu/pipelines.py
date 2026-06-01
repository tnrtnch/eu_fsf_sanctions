import json
from pathlib import Path
from datetime import datetime, UTC


class EuPipeline:
    def open_spider(self, spider):
        spider.logger.info("PIPELINE OPENED")

        self.items = []

        output_file = spider.config.get("output_file")

        spider.logger.info(f"OUTPUT FILE: {output_file}")

        if not output_file:
            raise Exception("output_file missing in scraper.yaml")

        self.json_path = Path(output_file).resolve()

        spider.logger.info(f"JSON PATH: {self.json_path}")

    def process_item(self, item, spider):
        spider.logger.info(f"PROCESS ITEM: {item}")

        self.items.append(dict(item))

        return item

    def close_spider(self, spider):
        spider.logger.info("CLOSING SPIDER")
        if len(self.items) < 100:
            raise Exception(
                f"Refusing to write suspicious dataset "
                f"with only {len(self.items)} items"
            )

        output = {
            "generated_at": datetime.now(UTC).isoformat(),
            "items": self.items
        }

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(
                output,
                f,
                ensure_ascii=False,
                indent=2
            )

        spider.logger.info(
            f"{len(self.items)} records written to {self.json_path}"
        )
