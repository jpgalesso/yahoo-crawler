from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from crawler.parser import YahooParser

import pandas as pd
import time


class YahooCrawler:

    def __init__(self, region):
        self.region = region
        self.url = "https://finance.yahoo.com/research-hub/screener/equity/"
        self.driver = self._start_driver()
        self.data = []

    def _start_driver(self):
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        return webdriver.Chrome(service=service, options=options)

    def access_page(self):
        self.driver.get(self.url)

        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        time.sleep(3)
        self._apply_region_filter()

    def _apply_region_filter(self):
        try:
            region_button = self.driver.find_element(By.XPATH, "//button[contains(., 'Region')]")
            region_button.click()
            time.sleep(2)

            region_option = self.driver.find_element(By.XPATH, f"//span[contains(text(), '{self.region}')]")
            region_option.click()
            time.sleep(2)

            apply_button = self.driver.find_element(By.XPATH, "//button[contains(., 'Apply')]")
            apply_button.click()

            time.sleep(5)

        except Exception as e:
            print("Erro ao aplicar filtro:", e)

    def extract_data(self):
        html = self.driver.page_source
        parser = YahooParser()
        self.data = parser.parse(html)

    def save_csv(self):
        df = pd.DataFrame(self.data)
        df.to_csv("output.csv", index=False)

    def run(self):
        try:
            self.access_page()
            self.extract_data()
            self.save_csv()
        finally:
            self.driver.quit()
