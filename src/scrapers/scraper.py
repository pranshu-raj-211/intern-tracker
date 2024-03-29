import random
import logging
import time
from abc import ABC, abstractmethod
from typing import Dict
from datetime import datetime
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium.common.exceptions import TimeoutException

class Scraper:
    def __init__(self, url: str, pagination_limit:int, source: str) -> None:
        self.url = url
        self.pagination_limit = pagination_limit
        self.source = source
        self.date = datetime.now().strftime('%Y_%m_%d')
        self.save_path = f'data/raw/{self.source}/{self.date}.csv'
        self.driver = webdriver.Firefox()
        self.all_data = pd.DataFrame()

    @abstractmethod
    def parse_soup(self,soup:BeautifulSoup) -> Dict[str,str]:
        pass

    @abstractmethod
    def fetch_and_parse_html(self):
        pass
        
    def save_data(self):
        self.all_data.to_csv(self.save_path, index=False)

    def scrape(self):
        try:
            self.fetch_and_parse_html()
        except TimeoutException:
            logging.error('Timeout')
        finally:
            self.driver.quit()