import logging
import time

import requests


class BaseScraper:
    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; PracticeScraper/1.0)"
        })

        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url):
        retries = 3
        retry_status_codes = {429, 500, 502, 503, 504}

        for attempt in range(1, retries + 1):
            try:
                response = self.session.get(url, timeout=15)

                if response.status_code == 200:
                    time.sleep(0.5)
                    return response.text

                if response.status_code in retry_status_codes:
                    self.logger.warning(
                        "Temporary HTTP error %s for %s (attempt %s/%s)",
                        response.status_code,
                        url,
                        attempt,
                        retries
                    )

                    if attempt < retries:
                        time.sleep(2 ** (attempt - 1))
                        continue

                response.raise_for_status()

            except requests.RequestException as error:
                self.logger.error(
                    "Request failed for %s: %s",
                    url,
                    error
                )

                if attempt < retries:
                    time.sleep(2 ** (attempt - 1))
                    continue

                return None

        return None