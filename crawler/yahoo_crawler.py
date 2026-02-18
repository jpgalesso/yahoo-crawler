from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from crawler.parser import YahooParser

import pandas as pd
import time
import os
import logging
from datetime import datetime
import re


class YahooCrawler:

    def __init__(self, region):
        self.region = region
        self.sanitized_region = self._sanitize_name(region)
        self.url = "https://finance.yahoo.com/research-hub/screener/equity/?start=0&count=100"
        self.driver = self._start_driver()
        self.data = []
        self.start_time = None
        self._setup_logging()

    def _start_driver(self):
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        return webdriver.Chrome(service=service, options=options)

    def _sanitize_name(self, name):
        return re.sub(r'[^A-Za-z0-9_-]', '_', name.strip())

    def _setup_logging(self):
        os.makedirs("exports/logs", exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        logging.basicConfig(
            filename=f"exports/logs/execution_{self.sanitized_region}_{ts}.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    # ---------------------------------------------------

    def access_page(self):
        self.driver.get(self.url)

        wait = WebDriverWait(self.driver, 5)  # ⬅ timeout reduzido
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        time.sleep(1)
        self._apply_region_filter()
        self._change_page_size_to_100()

    # ---------------------------------------------------
    # REMOVE US + APPLY REGION
    # ---------------------------------------------------

    def _apply_region_filter(self):
        try:
            region_button = self.driver.find_element(
                By.XPATH, "//button[contains(., 'Region')]"
            )
            region_button.click()
            time.sleep(0.5)

            # remove United States se marcado
            try:
                us = self.driver.find_element(
                    By.XPATH,
                    "//span[contains(text(),'United States')]"
                )
                self.driver.execute_script("arguments[0].click();", us)
                time.sleep(0.2)
            except:
                pass

            # marca região desejada
            region_option = self.driver.find_element(
                By.XPATH,
                f"//span[contains(text(),'{self.region}')]"
            )
            self.driver.execute_script("arguments[0].click();", region_option)

            apply_btn = self.driver.find_element(
                By.XPATH,
                "//button[contains(., 'Apply')]"
            )
            apply_btn.click()

            time.sleep(1)

        except Exception as e:
            logging.error(f"Erro filtro região: {e}")

    # ---------------------------------------------------
    # ALTERA PAGE SIZE PARA 100
    # ---------------------------------------------------

    def _change_page_size_to_100(self):
        try:
            print("Alterando resultados por página para 100...")

            dropdown = self.driver.find_element(
                By.XPATH,
                "//button[contains(@aria-label,'Rows per page')]"
            )

            dropdown.click()
            time.sleep(0.2)

            option_100 = self.driver.find_element(
                By.XPATH,
                "//span[text()='100']"
            )

            self.driver.execute_script("arguments[0].click();", option_100)

            time.sleep(1)

        except Exception as e:
            logging.warning(f"Não foi possível alterar page size: {e}")

    # ---------------------------------------------------
    # PAGINATION (ANCHOR CORRETA)
    # ---------------------------------------------------

    def extract_all_pages(self):

        parser = YahooParser()
        page = 1

        while True:

            print(f"Extraindo página {page}...")

            html = self.driver.page_source
            self.data.extend(parser.parse(html))

            try:
                next_btn = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button[data-testid='next-page-button']"
                )

                # se desabilitado -> fim
                if next_btn.get_attribute("disabled"):
                    break

                self.driver.execute_script(
                    "arguments[0].scrollIntoView();",
                    next_btn
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    next_btn
                )

                page += 1
                time.sleep(1)

            except NoSuchElementException:
                break

    # ---------------------------------------------------

    def save_csv(self):

        df = pd.DataFrame(self.data)
        df.drop_duplicates(inplace=True)

        now = datetime.now()

        export_path = os.path.join(
            "exports",
            self.sanitized_region,
            now.strftime("%Y"),
            now.strftime("%m"),
            now.strftime("%d")
        )

        os.makedirs(export_path, exist_ok=True)

        filename = f"output_{self.sanitized_region}_{now.strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(export_path, filename)

        df.to_csv(filepath, index=False)

        print(f"\nArquivo salvo em: {filepath}")
        print(f"Total exportado: {len(df)}")

    # ---------------------------------------------------

    def run(self):

        self.start_time = time.time()

        try:
            self.access_page()
            self.extract_all_pages()
            self.save_csv()

        finally:
            self.driver.quit()
            total = round(time.time() - self.start_time, 2)
            print(f"\nTempo total: {total} segundos")
