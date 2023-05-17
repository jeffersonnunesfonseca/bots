import json
import logging
import time
import pandas as pd
import os
import re
import random
from unidecode import unidecode
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import exceptions as selenium_ex
from bots.selenium import Selenium
from bots import utils

LOGGER = logging.getLogger(__name__)
SITE_URL = 'https://www.google.com/maps/'

SEARCH_INPUT_XPATH = '//*[@id="searchboxinput"]'

DATA_COMPANY_XPATH_NEW = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[{cont}]'
DATA_COMPANY_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]'
DATA_COMPANY_XPATH_TRY = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]'
COMPANIES_SIDE_BAR = '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/div/a'

LOGGER = logging.getLogger(__name__)

class GetDataByGoogleMaps:

    def __init__(self) -> None:
        self.path_to_companies = None
        self.last_cpf_cnpj = None
        self._driver = None
        self.only_cellphone = False

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
                if type(self._driver).__name__ == 'WebDriver':
                    self._driver.quit()

                self._get_session()
                LOGGER.info(f"acessando url {SITE_URL}")
                self._driver.get(SITE_URL)
                
                LOGGER.info("maximizando")
                self._driver.maximize_window()

                LOGGER.info(f"escrevendo no input")
                input_search = self._driver.find_element(By.XPATH, SEARCH_INPUT_XPATH)
                input_search.send_keys(row['fantasy_name'])
                input_search.send_keys(Keys.RETURN)
                time.sleep(5)

                try:
                    LOGGER.info("Buscando bloco de dados...")    
                    
                    block = self._driver.find_element(By.XPATH, DATA_COMPANY_XPATH)
                    LOGGER.info("scroll to btn")            
                    self._driver.execute_script("arguments[0].scrollIntoView();", block)
                    block = block.text
                    if not block:
                        block = self._driver.find_element(By.XPATH, DATA_COMPANY_XPATH_TRY)
                        LOGGER.info("scroll to btn")            
                        self._driver.execute_script("arguments[0].scrollIntoView();", block)
                        block = block.text
                        if not block:
                            raise Exception("block 2 not found")
                    infos = block.split("\n")
                    address = None
                    phone = None
                    site = None

                    regex_address = re.compile(r'(\d{5}-\d{3})')
                    regex_phone = re.compile(r'^([()\d\s]+)([\d-]+)$')
                    regex_site = re.compile(r'^(http(s?):\/\/)?(www\.)?[a-zA-Z0-9\.\-\_]+(\.[a-zA-Z]{2,3})+(\/[a-zA-Z0-9\_\-\s\.\/\?\%\#\&\=]*)?$')

                    for info in infos:
                        if "," in info:
                           if regex_address.search(info):
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
                    
                    phone = str(self._only_numbers(phone))
                    
                    if self.only_cellphone and not self.is_cellphone(phone):
                        raise Exception("phone not is cellphone")

                    if phone[0:2] != "55":
                        phone = f"55{phone}"
                    
                    data = {
                        "fantasy_name": row['fantasy_name'],
                        "phone": phone,
                        "cnpj": row['cnpj'],
                        "address": address,
                        "site": site
                    }
                    df_data = pd.DataFrame([data])
                    

                    # incrementa o arquivo caso exista, assim se der erro, nao perde oq ja conseguiu
                    if not os.path.isfile(filename):
                        df_data.to_csv(filename, sep=";", index=False)
                    else: # else it exists so append without writing the header
                        df_data.to_csv(filename, sep=";", index=False, mode='a', header=False)
                    
                except Exception as ex:
                    LOGGER.info(f"{row['fantasy_name']} - Não encontrado")
                    if "Unable to locate element" in str(ex):
                        ex = "block 1 not found"
                        
                    data_not_found = {
                        "fantasy_name": row['fantasy_name'],
                        "cnpj": row['cnpj'],
                        "exception": str(ex)
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

    def is_cellphone(self, cellphone):
        CELLPHONE_RE = re.compile(r'\b\d{2}[6789]\d*\b')
        return CELLPHONE_RE.match(cellphone)
   
    def _only_numbers(self, string: str):
        if not string:
            return None
        
        return int(''.join(i for i in string if i.isdigit()))

class GetDataGoogleMapsByTerm(Selenium):
    """ Busca dados do google maps a partir de um termo de busca, exemplo:
        term=comércio em campo de santana ,tatuquara e região
    """
    URL_BASE = "https://www.google.com.br/maps/search/{term}"

    def __init__(self, term, path_to_save, remote_url=None) -> None:
        super().__init__(remote_url=remote_url)
        self.term = term # busca que deseja realizar coleta
        self.links = None
        self.last_link = None
        self.path_to_save = path_to_save

    def execute(self):
        try:
            self._get_session()
            if not self.links:
                url = self.URL_BASE.replace('{term}', str(self.term))
                self._access_url(url)
                self.links = self._get_internal_link_companies()

            total = len(self.links)
            LOGGER.info(f"Total links: {len(self.links)}")

            filename = f'{self.path_to_save}lead_{datetime.now().strftime("%Y%m%d")}.csv'         
            count_total_not_found = 0   
            
            for idx, link in enumerate(self.links):
                if self.last_link and link != self.last_link:
                    continue

                self.last_link = None
                LOGGER.info(f"[{idx} de {total}] [Total not found: {count_total_not_found}]")

                try:
                    data = self._get_data(link)
                    df_data = pd.DataFrame([data])                   

                    # incrementa o arquivo caso exista, assim se der erro, nao perde oq ja conseguiu
                    if not os.path.isfile(filename):
                        df_data.to_csv(filename, sep=";", index=False)
                    else: # else it exists so append without writing the header
                        df_data.to_csv(filename, sep=";", index=False, mode='a', header=False)

                except selenium_ex.NoSuchElementException as ex:
                    count_total_not_found+=1
                    continue

                except Exception as ex:
                    print(ex)
                    import ipdb;ipdb.set_trace()
   
            LOGGER.info(f"[Fim][Total nao encontrado: {count_total_not_found}]")
        finally:
            self._driver.quit()
   
    def _get_internal_link_companies(self):
        """ corre empresas da barra lateral extraindo os links internos"""
        links = []
        old_len_link = 0
        scroll_count = 0
        count_without_link = 0
        while True:
            if links and len(links) > 5 and len(links) == old_len_link:
                LOGGER.info("chegou ao final da lista")
                break

            old_len_link = len(links)

            for x in range(0, 10):
                if x ==0 and len(links) == 0:
                    companies = self._wait_elements_by_xpath(COMPANIES_SIDE_BAR)
                    companies[0].click()
                    utils.force_time_sleep(3, "primeiro click")

                utils.force_time_sleep(random.choice(range(1, 5)), f'scrollando side bar {scroll_count}')                    
                self._wait_element_by_xpath('/html').send_keys(Keys.PAGE_DOWN)
                scroll_count +=1

            companies = self._wait_elements_by_xpath(COMPANIES_SIDE_BAR)
            for company in companies:
                href = company.get_attribute('href')
                if not href:
                    count_without_link +=1
                    LOGGER.info(f"sem link: {count_without_link}")
                    continue

                links.append(href)
            
            try:
                # clica no ultimo elemento para poder habilitar o scrolls
                company.click()
            except selenium_ex.ElementClickInterceptedException:
                continue

            links = list(set(links))
            LOGGER.info(f"[Total scrolls: {scroll_count}] [Total links: {len(links)}] [Sem link: {count_without_link}]")
        
        return links

    def _get_data(self, url):
        self._access_url(url)

        # estrutura sempre é a mesma porém muda a posição da div
        div = 1
        limit = 100
        while True:
            if div >= limit:
                raise selenium_ex.NoSuchElementException('passou de div 100')

            LOGGER.info(f"tentando localizar na div: {div}")
            block = self._driver.find_element(By.XPATH, DATA_COMPANY_XPATH_NEW.replace('{cont}', str(div)))
            if utils.has_cep(block.text):
                break
            div +=1

        self._driver.execute_script("arguments[0].scrollIntoView();", block)
        block = self._driver.find_element(By.XPATH, DATA_COMPANY_XPATH_NEW.replace('{cont}', str(div)))
        if not block.text:
            return False

        infos = block.text.split("\n")
        address = None
        phone = None
        site = None
        type = None
        name = None

        regex_address = re.compile(r'(\d{5}-\d{3})')
        regex_phone = re.compile(r'^([()\d\s]+)([\d-]+)$')
        regex_site = re.compile(r"((http|https)://)?(www.)?" +
                                "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                                "{2,256}\\.[a-z]" +
                                "{2,6}\\b([-a-zA-Z0-9@:%" +
                                "._\\+~#?&//=]*)")        
        for info in infos:
            if "," in info:
                if regex_address.search(info):
                    address = info
                    continue

            if regex_phone.match(info):
                phone = info
                continue 

            if regex_site.match(info):
                site = info
                continue 
        
        if phone:
            phone = str(utils.only_numbers(phone))
            type = "CELLPHONE" if utils.is_cellphone(phone) else "PHONE"
        
        name = self._wait_element_by_xpath(SEARCH_INPUT_XPATH).get_attribute('value')

        data = {
            "url": url.split('/data')[0],
            "type": type, 
            "phone": phone,
            "address": address,
            "site": site,
            "name": name,
            "site": site
        }        
        return data