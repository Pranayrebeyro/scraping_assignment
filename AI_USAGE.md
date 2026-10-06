# AI Usage

## Overview

ChatGPT was used during the development of this Python web scraping assignment as a development, debugging, and review assistant.

The final implementation was reviewed, modified where necessary, tested locally, and verified against the assignment requirements before submission.

AI assistance was mainly used to help understand requirements, discuss implementation approaches, troubleshoot development issues, review logic, suggest test cases, and improve documentation.

The final implementation decisions and verification were performed as part of the development process rather than relying on AI output without testing.

---

## AI Tool Used

### ChatGPT

ChatGPT was used throughout the development process as an assistant for:

- Understanding the assignment requirements
- Breaking the assignment into implementation steps
- Discussing the project structure
- Understanding the HTML structure of the practice websites
- Discussing pagination approaches
- Reviewing scraping logic
- Reviewing data-cleaning approaches
- Reviewing validation rules
- Discussing duplicate-detection strategies
- Troubleshooting Python and testing issues
- Suggesting unit-test cases
- Reviewing documentation
- Identifying possible edge cases

AI-generated suggestions were reviewed before being incorporated into the project.

---

## Representative Prompts

The following are representative examples of the types of prompts used during development.

### Project Planning

> "Help me break down this Python web scraping interview assignment into manageable implementation steps."

### Project Structure

> "Suggest a clean Python project structure for separating source scrapers, data processing, tests, outputs and logs."

### Scraping Approach

> "What is a suitable Requests and BeautifulSoup approach for scraping Books to Scrape and following the next-page link dynamically?"

### Quotes Scraping

> "Review the HTML structure of Quotes to Scrape and suggest how the quote text, author and tags can be extracted."

### Data Cleaning

> "Review a cleaning approach for whitespace, prices, ratings, tags and missing values according to the assignment requirements."

### Validation

> "Suggest validation rules for source, title, URL, price and rating for this standardized dataset."

### Duplicate Detection

> "Suggest a reliable duplicate-detection strategy that handles differences in capitalization, whitespace and punctuation."

### Testing

> "Suggest unit test cases for cleaning, validation and deduplication that do not require internet access."

### Troubleshooting

> "Pytest cannot find the processing package. Help me diagnose the Python import issue."

### Documentation

> "Review the README structure and identify whether it covers the assignment's required documentation points."

---

## Areas Where AI Assisted

### 1. Project Structure

AI was used to discuss a modular structure that separates scraping, processing, testing and output generation.

The final project structure is:

```text
scraping_assignment/
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
├── tests/
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
├── output/
├── logs/
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md