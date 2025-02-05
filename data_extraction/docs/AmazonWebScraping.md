# Amazon Web Scraping #

Note sul web scraping fatto su Amazon

## Campi da estrarre ##

| Caratteristiche                                       | Proprietà                       | Descrizione                                                             | Acquisite/Ricavate | Function                                      |
|-------------------------------------------------------|---------------------------------|-------------------------------------------------------------------------|--------------------|-----------------------------------------------|
| Prezzo totale                                         | seller.sale.totalPrice          | Somma tra il costo prodotto e costo spedizione                          | Ricavato           | price_no_shipping + seller_shipping_price     |
| Prezzo prodotto                                       | seller.sale.priceNoShipping     | Costo effettivo del prodotto al netto della spedizione                  | Acquisito          | get_price_buybox_winner                       |
| Numero di valutazioni Prodotto                        | product.ratings.num             | Numero di recensioni dei clienti per il prodotto                        | Acquisito          | get_product_num_ratings                       |
| Numero di valutazioni Venditore                       | seller.ratings.num              | Numero di recensioni dei clienti per il venditore                       | Acquisito          | get_seller_num_ratings                        |
| Media valutazioni                                     | seller.ratings.avg              | Media delle valutazioni dei clienti da 0 a 5 stelle                     | Acquisito          | get_seller_avg_ratings                        |
| Percentuale valutazioni positive                      | seller.ratings.perc_positive    | Rappresenta la percentuale di valutazioni positive negli ultimi 12 mesi | Acquisito          | get_seller_perc_positive_ratings              |
| FBA                                                   | seller.fba                      | Determina se il venditore aderisce o meno alla logistica di Amazon      | Acquisito          | get_seller_fba                                |
| Prezzo spedizione                                     | seller.shipping.price           | Rappresenta il costo di spedizione                                      | Acquisito          | get_seller_shipping_price                     |
| Giorni consegna                                       | seller.shipping.days            | Determina la stima di quando il prodotto verrà consegnato al cliente    | Acquisito          | get_seller_shipping_days                      |
| Amazon come venditore                                 | seller.name contains "Amazon"   | Verifica se il venditore è Amazon                                       | Acquisito          | seller.name contains "Amazon"                 |
| Differenza prezzo da buy box winner                   | seller.sale.diffTotalPrice      | Differenza prezzo da buy box winner                                     | Ricavato           | total_price - buybox_total_price              |
| Differenza prezzo da buy box winner (solo prodotto)   | seller.sale.diffPriceNoShipping | Differenza prezzo da buy box winner (solo prodotto)                     | Ricavato           | price_no_shipping - buybox_price_no_shipping  |
| Differenza prezzo da buy box winner (solo spedizione) | seller.shipping.diffPrice       | Differenza prezzo da buy box winner (solo spedizione)                   | Ricavato           | seller_shipping_price - buybox_shipping_price |
| Buy Box Winner                                        | index == 0                      | Indica se il venditore ha vinto il buy box                              | Acquisito          | index == 0                                    |


## Algoritmi di web scraping ##

### Librerie utilizzate ###

Le librerie utilizzate per il Web Scraping da Amazon sono le seguenti:
* Selenium
* BeautifulSoap
* Lxml


## Salvataggio dati ##

I dati estratti sono normalizzati e strutturati in formato JSON, in modo da rendere semplice il successivo salvataggio
in un database non-relazionale.

### Mongo DB ###

Viene usato un database non-relazionale (MongoDB) per il salvataggio dei dati estratti in formato JSON.

## Containerizzazione ##

### Docker ###

#### Creazione Immagine Docker ####

Comando: `docker build -t amazon-buybox:1.0.0 .`

#### Start Container con immagine Docker ####

Comando: `docker run amazon-buybox:1.0.0`

### Compose ###

Comando: `docker compose up`