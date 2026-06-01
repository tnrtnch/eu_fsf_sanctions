import json
from pathlib import Path
from datetime import datetime, UTC


class EuPipeline:

    def open_spider(self, spider):
        spider.logger.info("PIPELINE OPENED")

        self.items = []

        self.json_path = Path(
            "eu_fsf_sanctions.json"
        ).resolve()

        spider.logger.info(
            f"JSON PATH: {self.json_path}"
        )

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        spider.logger.info("CLOSING SPIDER")

        if len(self.items) < 100:
            raise Exception(
                f"Too few items: {len(self.items)}"
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
            f"{len(self.items)} records written"
        )
