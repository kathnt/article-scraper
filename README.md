# article-scraper
Retrieves article title and relevant info from database given publisher info and keyword.

- `article-scrape-downloader.py` downloads article info as Excel files
  - lists article title, publisher, and date published
- `xlsx-to-csv.py` converts the Excel files into csv files
- `csv-remove-duplicate.py` removes duplicate articles from a csv file
  - based on similartiy score and data published
