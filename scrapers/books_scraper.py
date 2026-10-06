from datetime import datetime, timezone
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base_scraper import BaseScraper


class BooksScraper(BaseScraper):
    BASE_URL = "https://books.toscrape.com/"

    def scrape(self):
        records = []
        current_url = self.BASE_URL

        while current_url:
            self.logger.info("Scraping books page: %s", current_url)

            html = self.fetch_page(current_url)

            if not html:
                self.logger.error("Could not retrieve books page: %s", current_url)
                break

            soup = BeautifulSoup(html, "html.parser")
            books = soup.select("article.product_pod")

            if not books:
                self.logger.warning("No books found on page: %s", current_url)

            for book in books:
                record = self._parse_book(book, current_url)

                if record:
                    records.append(record)

            next_link = soup.select_one("li.next a")

            if next_link and next_link.get("href"):
                current_url = urljoin(current_url, next_link["href"])
            else:
                current_url = None

        self.logger.info("Books scraping completed. Records found: %s", len(records))

        return records

    def _parse_book(self, book, page_url):
        try:
            title_link = book.select_one("h3 a")
            price_element = book.select_one("p.price_color")
            rating_element = book.select_one("p.star-rating")

            if not title_link:
                self.logger.warning("Book title is missing on %s", page_url)
                return None

            title = title_link.get("title") or title_link.get_text(strip=True)

            if not title:
                self.logger.warning("Book title is empty on %s", page_url)
                return None

            price = None

            if price_element:
                price = price_element.get_text(strip=True)

            rating = None

            if rating_element:
                rating_classes = rating_element.get("class", [])

                for rating_class in rating_classes:
                    if rating_class in {"One", "Two", "Three", "Four", "Five"}:
                        rating = rating_class
                        break

            book_url = None

            if title_link.get("href"):
                book_url = urljoin(page_url, title_link["href"])

            return {
                "source": "Books to Scrape",
                "source_url": book_url or page_url,
                "name_or_title": title,
                "category": None,
                "price": price,
                "rating": rating,
                "author": None,
                "tags": None,
                "description": None,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as error:
            self.logger.warning(
                "Could not parse a book on %s: %s",
                page_url,
                error
            )
            return None