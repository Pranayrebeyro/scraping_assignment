from processing.cleaning import (
    clean_price,
    clean_rating,
    clean_record,
    clean_tags,
    clean_text,
)


def test_clean_text():
    assert clean_text("  Hello    world  ") == "Hello world"
    assert clean_text("   ") is None
    assert clean_text(None) is None


def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price("  £10.50 ") == 10.50
    assert clean_price(None) is None
    assert clean_price("invalid") is None


def test_clean_rating():
    assert clean_rating("One") == 1
    assert clean_rating("Three") == 3
    assert clean_rating("Five") == 5
    assert clean_rating("4") == 4
    assert clean_rating("7") is None


def test_clean_tags():
    assert clean_tags("life;  change; inspiration") == (
        "life; change; inspiration"
    )

    assert clean_tags(["life", "change"]) == "life; change"

    assert clean_tags(None) is None


def test_clean_record():
    record = {
        "source": " Books to Scrape ",
        "source_url": " https://example.com/book ",
        "name_or_title": "  A   Book  ",
        "category": None,
        "price": "£20.50",
        "rating": "Four",
        "author": None,
        "tags": None,
        "description": None,
        "scraped_at": " 2026-10-06T10:00:00Z ",
    }

    cleaned = clean_record(record)

    assert cleaned["source"] == "Books to Scrape"
    assert cleaned["name_or_title"] == "A Book"
    assert cleaned["price"] == 20.50
    assert cleaned["rating"] == 4