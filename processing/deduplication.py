import hashlib
import re


def normalize_for_duplicate(value):
    if value is None:
        return ""

    value = str(value).lower()
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value


def create_duplicate_key(record):
    source = normalize_for_duplicate(record.get("source"))

    if record.get("source") == "Books to Scrape":
        title = normalize_for_duplicate(record.get("name_or_title"))
        raw_key = f"{source}|{title}"

    elif record.get("source") == "Quotes to Scrape":
        author = normalize_for_duplicate(record.get("author"))
        quote = normalize_for_duplicate(record.get("name_or_title"))
        quote = quote[:50]

        raw_key = f"{source}|{author}|{quote}"

    else:
        title = normalize_for_duplicate(record.get("name_or_title"))
        raw_key = f"{source}|{title}"

    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def remove_duplicates(records):
    unique_records = []
    seen_keys = set()
    duplicate_count = 0

    for record in records:
        duplicate_key = create_duplicate_key(record)

        if duplicate_key in seen_keys:
            duplicate_count += 1
            continue

        seen_keys.add(duplicate_key)
        unique_records.append(record)

    return unique_records, duplicate_count