# Python Web Scraping ETL Pipeline

A Python-based web scraping and ETL pipeline that collects practice data from two public websites, cleans and validates the records, removes duplicates, and produces a consolidated dataset with a summary report.

## Sources

The project scrapes the following public practice websites:

- Books to Scrape — https://books.toscrape.com/
- Quotes to Scrape — https://quotes.toscrape.com/

---

## Project Overview

The pipeline follows this workflow:

```text
Books to Scrape ──┐
                  ├──> Scrape ──> Clean ──> Validate ──> Deduplicate ──> Output
Quotes to Scrape ─┘