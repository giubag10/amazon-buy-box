# Import/Export dati da MongoDB

## Come esportare i dati di scraping da MongoDB in JSON

1. Lanciare il seguente comando dalla cartella root del progetto:
```pycon
python .\data_import_export\scripts\amazon_data_exporter.py
```

## Come importare i dati di scraping esportati in JSON

1. Copiare il file esportato precedentemente nella cartella root del progetto
2. Lanciare il seguente comando dalla cartella root del progetto:
```pycon
python .\data_import_export\scripts\amazon_data_importer.py ".\scraping_data_export_2024-09-09_2025-01-01.json"
```