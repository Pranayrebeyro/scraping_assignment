from processing.validation import validate_record, validate_records


def make_valid_record():
    return {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/catalogue/book.html",
        "name_or_title": "A Book",
        "category": None,
        "price": 25.50,
        "rating": 4,
        "author": None,
        "tags": None,
        "description": None,
        "scraped_at": "2026-10-06T10:00:00+00:00",
    }


def test_valid_record():
    record = make_valid_record()

    is_valid, errors = validate_record(record)

    assert is_valid is True
    assert errors == []


def test_missing_title():
    record = make_valid_record()
    record["name_or_title"] = None

    is_valid, errors = validate_record(record)

    assert is_valid is False
    assert "missing name_or_title" in errors


def test_invalid_url():
    record = make_valid_record()
    record["source_url"] = "not-a-url"

    is_valid, errors = validate_record(record)

    assert is_valid is False
    assert "invalid source_url" in errors


def test_invalid_price():
    record = make_valid_record()
    record["price"] = -10

    is_valid, errors = validate_record(record)

    assert is_valid is False
    assert "invalid price" in errors


def test_invalid_rating():
    record = make_valid_record()
    record["rating"] = 7

    is_valid, errors = validate_record(record)

    assert is_valid is False
    assert "invalid rating" in errors


def test_validate_records():
    valid_record = make_valid_record()

    invalid_record = make_valid_record()
    invalid_record["name_or_title"] = None

    valid, rejected = validate_records([
        valid_record,
        invalid_record,
    ])

    assert len(valid) == 1
    assert len(rejected) == 1
    assert "missing name_or_title" in rejected[0]["reasons"]