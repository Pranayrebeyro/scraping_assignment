from urllib.parse import urlparse


VALID_SOURCES = {
    "Books to Scrape",
    "Quotes to Scrape",
}


def validate_url(url):
    if not url:
        return False

    parsed = urlparse(url)

    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_record(record):
    errors = []

    source = record.get("source")
    source_url = record.get("source_url")
    name_or_title = record.get("name_or_title")
    price = record.get("price")
    rating = record.get("rating")

    if source not in VALID_SOURCES:
        errors.append("invalid source")

    if not name_or_title:
        errors.append("missing name_or_title")

    if not validate_url(source_url):
        errors.append("invalid source_url")

    if price is not None:
        if not isinstance(price, (int, float)) or price < 0:
            errors.append("invalid price")

    if rating is not None:
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            errors.append("invalid rating")

    return len(errors) == 0, errors


def validate_records(records):
    valid_records = []
    rejected_records = []

    for record in records:
        is_valid, errors = validate_record(record)

        if is_valid:
            valid_records.append(record)
        else:
            rejected_records.append({
                "record": record,
                "reasons": errors,
            })

    return valid_records, rejected_records