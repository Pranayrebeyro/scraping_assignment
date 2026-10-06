from datetime import datetime, timezone
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base_scraper import BaseScraper


class QuotesScraper(BaseScraper):
    BASE_URL = "https://quotes.toscrape.com/"

    def scrape(self):
        records = []
        current_url = self.BASE_URL

        while current_url:
            self.logger.info("Scraping quotes page: %s", current_url)

            html = self.fetch_page(current_url)

            if not html:
                self.logger.error("Could not retrieve quotes page: %s", current_url)
                break

            soup = BeautifulSoup(html, "html.parser")
            quotes = soup.select("div.quote")

            if not quotes:
                self.logger.warning("No quotes found on page: %s", current_url)

            for quote in quotes:
                record = self._parse_quote(quote, current_url)

                if record:
                    records.append(record)

            next_link = soup.select_one("li.next a")

            if next_link and next_link.get("href"):
                current_url = urljoin(current_url, next_link["href"])
            else:
                current_url = None

        self.logger.info(
            "Quotes scraping completed. Records found: %s",
            len(records)
        )

        return records

    def _parse_quote(self, quote, page_url):
        try:
            text_element = quote.select_one("span.text")
            author_element = quote.select_one("small.author")
            tag_elements = quote.select("a.tag")

            if not text_element:
                self.logger.warning("Quote text is missing on %s", page_url)
                return None

            quote_text = text_element.get_text(" ", strip=True)

            if not quote_text:
                self.logger.warning("Quote text is empty on %s", page_url)
                return None

            author = None

            if author_element:
                author = author_element.get_text(" ", strip=True)

            tags = []

            for tag in tag_elements:
                tag_text = tag.get_text(" ", strip=True)

                if tag_text:
                    tags.append(tag_text)

            author_link = quote.select_one('a[href^="/author/"]')

            source_url = page_url

            if author_link and author_link.get("href"):
                source_url = urljoin(page_url, author_link["href"])

            return {
                "source": "Quotes to Scrape",
                "source_url": source_url,
                "name_or_title": quote_text,
                "category": None,
                "price": None,
                "rating": None,
                "author": author,
                "tags": "; ".join(tags) if tags else None,
                "description": None,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as error:
            self.logger.warning(
                "Could not parse a quote on %s: %s",
                page_url,
                error
            )
            return None