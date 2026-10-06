import re


def clean_text(value):
    if value is None:
        return None

    value = str(value)
    value = re.sub(r"\s+", " ", value).strip()

    return value or None


def clean_price(value):
    if value is None:
        return None

    value = clean_text(value)

    if not value:
        return None

    value = re.sub(r"[^0-9.]", "", value)

    if not value:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def clean_rating(value):
    if value is None:
        return None

    rating_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
    }

    value = clean_text(value)

    if not value:
        return None

    normalized = value.lower()

    if normalized in rating_map:
        return rating_map[normalized]

    try:
        rating = int(float(normalized))

        if 1 <= rating <= 5:
            return rating

    except ValueError:
        pass

    return None


def clean_tags(value):
    if value is None:
        return None

    if isinstance(value, list):
        tags = [clean_text(tag) for tag in value]
        tags = [tag for tag in tags if tag]
        return "; ".join(tags) if tags else None

    value = clean_text(value)

    if not value:
        return None

    tags = [clean_text(tag) for tag in value.split(";")]
    tags = [tag for tag in tags if tag]

    return "; ".join(tags) if tags else None


def clean_record(record):
    cleaned = dict(record)

    cleaned["source"] = clean_text(cleaned.get("source"))
    cleaned["source_url"] = clean_text(cleaned.get("source_url"))
    cleaned["name_or_title"] = clean_text(cleaned.get("name_or_title"))
    cleaned["category"] = clean_text(cleaned.get("category"))
    cleaned["price"] = clean_price(cleaned.get("price"))
    cleaned["rating"] = clean_rating(cleaned.get("rating"))
    cleaned["author"] = clean_text(cleaned.get("author"))
    cleaned["tags"] = clean_tags(cleaned.get("tags"))
    cleaned["description"] = clean_text(cleaned.get("description"))
    cleaned["scraped_at"] = clean_text(cleaned.get("scraped_at"))

    return cleaned


def clean_records(records):
    cleaned_records = []

    for record in records:
        cleaned_records.append(clean_record(record))

    return cleaned_records