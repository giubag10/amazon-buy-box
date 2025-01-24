# amazon-buy-box

From the thesis "Unlocking the secrets of the Amazon Buy Box: a containerized approach" by Giulio Baglione

## Data Import/Export from MongoDB

### How to export scraping data to JSON from MongoDB

1. Run code below from dir root:
```pycon
python .\data_import_export\scripts\amazon_data_exporter.py
```

### How to import scraping data from JSON exported above

1. Copy exported file to dir root
2. Run code below from dir root:
```pycon
python .\data_import_export\scripts\amazon_data_importer.py ".\scraping_data_export_2024-09-09_2025-01-01.json"
```
