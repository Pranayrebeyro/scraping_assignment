from processing.deduplication import (
    create_duplicate_key,
    normalize_for_duplicate,
    remove_duplicates,
)


def test_normalize_for_duplicate():
    assert normalize_for_duplicate("  The Great Book!  ") == "the great book"
    assert normalize_for_duplicate("THE   GREAT   BOOK") == "the great book"


def test_book_duplicate_key():
    record_one = {
        "source": "Books to Scrape",
        "name_or_title": "The Great Book!",
    }

    record_two = {
        "source": "Books to Scrape",
        "name_or_title": "  the great book  ",
    }

    assert create_duplicate_key(record_one) == create_duplicate_key(record_two)


def test_quote_duplicate_key():
    record_one = {
        "source": "Quotes to Scrape",
        "author": "Albert Einstein",
        "name_or_title": "Life is beautiful and worth living.",
    }

    record_two = {
        "source": "Quotes to Scrape",
        "author": " albert einstein ",
        "name_or_title": "Life is beautiful and worth living.",
    }

    assert create_duplicate_key(record_one) == create_duplicate_key(record_two)


def test_remove_duplicates():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "The Great Book",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "the great book!",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "Another Book",
        },
    ]

    unique_records, duplicate_count = remove_duplicates(records)

    assert len(unique_records) == 2
    assert duplicate_count == 1