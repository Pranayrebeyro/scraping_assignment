import csv
import json
import logging
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from processing.cleaning import clean_records
from processing.deduplication import remove_duplicates
from processing.validation import validate_records
from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

CSV_FILE = OUTPUT_DIR / "final_dataset.csv"
JSON_FILE = OUTPUT_DIR / "summary_report.json"
LOG_FILE = LOG_DIR / "scraper.log"

CSV_FIELDS = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]


def setup_logging():
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def save_csv(records):
    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=CSV_FIELDS,
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerows(records)


def save_json(report):
    with JSON_FILE.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def run_scraper(scraper, source_name):
    logger = logging.getLogger(__name__)

    try:
        records = scraper.scrape()

        logger.info(
            "%s scraper returned %s records",
            source_name,
            len(records)
        )

        return records

    except Exception as error:
        logger.error(
            "%s scraper failed: %s",
            source_name,
            error
        )

        return []


def count_sources(records):
    return dict(Counter(
        record.get("source")
        for record in records
        if record.get("source")
    ))


def count_rejection_reasons(rejected_records):
    reasons = Counter()

    for rejected in rejected_records:
        for reason in rejected["reasons"]:
            reasons[reason] += 1

    return dict(reasons)


def main():
    setup_logging()

    logger = logging.getLogger(__name__)
    start_time = datetime.now(timezone.utc)

    logger.info("Scraping pipeline started")

    books_records = run_scraper(
        BooksScraper(),
        "Books to Scrape"
    )

    quotes_records = run_scraper(
        QuotesScraper(),
        "Quotes to Scrape"
    )

    raw_records = books_records + quotes_records

    raw_by_source = count_sources(raw_records)

    logger.info("Total raw records: %s", len(raw_records))

    cleaned_records = clean_records(raw_records)

    cleaned_by_source = count_sources(cleaned_records)

    logger.info(
        "Records after cleaning: %s",
        len(cleaned_records)
    )

    valid_records, rejected_records = validate_records(cleaned_records)

    for rejected in rejected_records:
        logger.warning(
            "Record rejected: %s",
            ", ".join(rejected["reasons"])
        )

    rejection_reasons = count_rejection_reasons(rejected_records)

    logger.info(
        "Valid records: %s",
        len(valid_records)
    )

    logger.info(
        "Rejected records: %s",
        len(rejected_records)
    )

    final_records, duplicate_count = remove_duplicates(valid_records)

    logger.info(
        "Duplicates removed: %s",
        duplicate_count
    )

    save_csv(final_records)

    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()

    report = {
        "run": {
            "started_at": start_time.isoformat(),
            "finished_at": end_time.isoformat(),
            "duration_seconds": duration,
        },
        "records": {
            "raw_total": len(raw_records),
            "raw_by_source": raw_by_source,
            "after_cleaning_total": len(cleaned_records),
            "after_cleaning_by_source": cleaned_by_source,
            "rejected_total": len(rejected_records),
            "rejection_reasons": rejection_reasons,
            "duplicates_removed": duplicate_count,
            "final_total": len(final_records),
            "final_by_source": count_sources(final_records),
        },
        "output": {
            "csv_file": str(CSV_FILE),
        },
    }

    save_json(report)

    logger.info(
        "Final dataset saved: %s",
        CSV_FILE
    )

    logger.info(
        "Summary report saved: %s",
        JSON_FILE
    )

    logger.info(
        "Scraping pipeline completed in %.2f seconds",
        duration
    )


if __name__ == "__main__":
    main()