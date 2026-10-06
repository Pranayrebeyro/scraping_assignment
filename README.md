# Python Web Scraping ETL Pipeline

A Python-based web scraping and ETL pipeline that collects practice data from two public websites, cleans and standardizes the records, validates the results, detects duplicates, and produces a consolidated dataset with a summary report.

The project was developed as part of a Python web scraping technical assessment.

---

## Sources

The project scrapes the following public practice websites:

- Books to Scrape — https://books.toscrape.com/
- Quotes to Scrape — https://quotes.toscrape.com/

Both websites are public scraping practice sites provided for this type of exercise.

---

## Project Overview

The pipeline follows this workflow:

```text
Books to Scrape ──┐
                  ├──> Scrape ──> Clean ──> Validate ──> Deduplicate ──> Consolidate ──> Output
Quotes to Scrape ─┘