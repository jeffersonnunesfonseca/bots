import json
import logging
import time
import pandas as pd
import os
import re
from unidecode import unidecode
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

LOGGER = logging.getLogger(__name__)
SITE_URL = 'https://www.google.com/maps/'

SEARCH_INPUT_XPATH = '//*[@id="searchboxinput"]'

ADDRESS_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div/div[3]/div[1]'
SITE_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[6]/a/div/div[3]/div[1]'
PHONE_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[7]/button/div/div[3]/div[1]'
DATA_COMPANY_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]'

class GetDataByGoogleMaps:

    def __init__(self) -> None:
        self.path_to_companies = None
        self.last_cpf_cnpj = None
        self._driver = None

    def execute(self):
        try:
            df = pd.read_csv(self.path_to_companies, sep=';')
            total = len(df)
            cont = 0
            filename = f'/tmp/lead_{datetime.now().strftime("%Y%m%d")}.csv'
            filename_not_found = f'/tmp/not_found_lead_{datetime.now().strftime("%Y%m%d")}.csv'
            for index, row in df.iterrows():
                LOGGER.info(f"{cont} de {total} - {row['cnpj']}")
                if self.last_cpf_cnpj:
                    cont += 1
                    if row['cnpj'] != self.last_cpf_cnpj:
                        continue

                    self.last_cpf_cnpj = None
                    continue

                # sempre cria nova sessão para nao ser barrado pela cloudflare
                if type(self._driver) == 'selenium.webdriver.chrome.webdriver.WebDriver':
                    self._driver.quit()

                self._get_session()
                LOGGER.info(f"acessando url {SITE_URL}")
                self._driver.get(SITE_URL)

                LOGGER.info(f"escrevendo no input")
                input_search = self._driver.find_element(By.XPATH, SEARCH_INPUT_XPATH)
                input_search.send_keys(row['fantasy_name'])
                input_search.send_keys(Keys.RETURN)
                time.sleep(5)

                try:
                    LOGGER.info("Buscando bloco de dados")
                    block = self._driver.find_element(By.XPATH, DATA_COMPANY_XPATH).text
                    infos = block.split("\n")
                    address = None
                    phone = None
                    site = None

                    regex_address = re.compile(r'^([\w\s]+),([\d\s]+)-([\w\s]+),([\w\s]+)-([\w\s]+),([\w\s-]+)')
                    regex_phone = re.compile(r'^([()\d\s]+)([\d-]+)$')
                    regex_site = re.compile(r'^(http(s?):\/\/)?(www\.)?[a-zA-Z0-9\.\-\_]+(\.[a-zA-Z]{2,3})+(\/[a-zA-Z0-9\_\-\s\.\/\?\%\#\&\=]*)?$')

                    for info in infos:
                        if regex_address.match(info):
                            address = info
                            continue

                        if regex_phone.match(info):
                            phone = info
                            continue 

                        if regex_site.match(info):
                            site = info
                            continue 

                    LOGGER.info(f"endereço {address}")
                    LOGGER.info(f"site {site}")
                    LOGGER.info(f"phone {phone}")
                    if not phone:
                        raise Exception("not found phone")
                    data = {
                        "fantasy_name": row['fantasy_name'],
                        "cnpj": row['cnpj'],
                        "address": address,
                        "site": site,
                        "phone": phone
                    }
                    df_data = pd.DataFrame([data])

                    # incrementa o arquivo caso exista, assim se der erro, nao perde oq ja conseguiu
                    if not os.path.isfile(filename):
                        df_data.to_csv(filename, sep=";", index=False)
                    else: # else it exists so append without writing the header
                        df_data.to_csv(filename, sep=";", index=False, mode='a', header=False)
                    
                except Exception as ex:
                    LOGGER.info(f"{row['fantasy_name']} - Não encontrado")
                    data_not_found = {
                        "fantasy_name": row['fantasy_name'],
                        "cnpj": row['cnpj']
                    }                    
                    # gera um arquivo com nao encontrados para validar depois
                    df_data_not_found = pd.DataFrame([data_not_found])

                    # incrementa o arquivo caso exista, assim se der erro, nao perde oq ja conseguiu
                    if not os.path.isfile(filename_not_found):
                        df_data_not_found.to_csv(filename_not_found, sep=";", index=False)
                    else: # else it exists so append without writing the header
                        df_data_not_found.to_csv(filename_not_found, sep=";", index=False, mode='a', header=False)
                    
                    cont +=1
                    continue
                    
                cont +=1

        finally:            
            self._driver.quit()

    def _get_session(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        self._driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)