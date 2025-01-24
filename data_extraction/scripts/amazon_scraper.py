import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from amazon_scraping_functions import *
from logger import logging


def extract_page_html(url):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)

    try:
        driver.get(url)

        # Attendo che la pagina sia caricata con il popup dei cookies
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'sp-cc-rejectall-link')))

        # Negare il consenso dei cookies
        driver.find_element(By.XPATH, '//*[@id=\"sp-cc-rejectall-link\"]').click()

        # Attendo che la pagina sia effettivamente caricata
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'aod-pinned-offer')))  # Buy Box
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'aod-offer-list')))  # Altri venditori
        except TimeoutException:
            logging.exception("Timed out waiting for offer panel to load")

        # Filtro per i prodotti nuovi
        filter_button = driver.find_element(By.XPATH, '//*[@id=\"aod-filter-string\"]')  # bottone filtra
        if filter_button is not None and filter_button.is_displayed():
            try:
                filter_button.click()
                driver.find_element(By.XPATH, '//*[@id=\"new\"]/div/label').click()  # checkbox nuovo
                time.sleep(2)
            except ElementClickInterceptedException:
                logging.exception("Filter button not clickable")

        bs = BeautifulSoup(driver.page_source, 'lxml')
    finally:
        driver.quit()

    return bs


def scrape_amazon(url):
    try:
        bs = extract_page_html(url)
    except Exception as e:
        logging.exception("Errore scraping amazon page [" + url + "]")
        return None

    buybox_root = bs.find("div", {"id", "aod-pinned-offer"})  # Vincitore buy box
    offer_list = bs.find_all("div", {"id": "aod-offer"})  # Altri venditori

    product_name = get_product_name(buybox_root)
    product_num_ratings = get_product_num_ratings(buybox_root)
    buybox_seller_data = get_seller_info(buybox_root, 0, None)
    other_seller_data = get_other_seller_info(offer_list, buybox_seller_data)
    amazon_data_from_url = {
        "product": {
            "name": product_name,
            "ratings": {
                "num": product_num_ratings
            }
        },
        "buybox_seller": buybox_seller_data,
        "other_sellers": other_seller_data
    }
    return amazon_data_from_url


