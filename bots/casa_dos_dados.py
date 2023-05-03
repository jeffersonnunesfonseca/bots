import json
import logging
import time
import pandas as pd
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

LOGGER = logging.getLogger(__name__)

SITE_URL = "https://casadosdados.com.br/solucao/cnpj/pesquisa-avancada"
CHROME_DRIVER_PATH = "resources/linux-chromedriver"

CNAE_INPUT_XPATH = '//*[@id="__layout"]/div/div[2]/section/div[2]/div[2]/section/div/div/div/div/div[1]/input'
STATE_INPUT_XPATH = '//*[@id="__layout"]/div/div[2]/section/div[3]/div[2]/div/div/div/div/div[1]/input'
CITY_INPUT_XPATH = '//*[@id="__layout"]/div/div[2]/section/div[3]/div[3]/div/div/div/div/div[1]/input'
BUTTON_SEARCH_XPATH = '//*[@id="__layout"]/div/div[2]/section/div[6]/div/div[1]/button[1]'
BUTTON_NEXT_PAGE_XPATH = '//*[@id="__layout"]/div/div[2]/section/div[8]/div/nav/a[2]/span/i'
TOTAL_RESULTS_XPATH = '//*[@id="__layout"]/div/div[2]/section/div[9]/div[1]/div/div/div/div/p/b'
LINKS_AFTER_FILTER_XPATH = '//*[@id="__layout"]/div/div[2]/section/div[9]/div[1]/div/div/div/div/div/article/div/div/p/a'

CNPJ_XPATH = '//*[@id="__layout"]/div/div[2]/section[1]/div/div/div[4]/div[1]/div[1]/div[1]/p[2]'
FANTASY_NAME_XPATH = '//*[@id="__layout"]/div/div[2]/section[1]/div/div/div[4]/div[1]/div[1]/div[3]/p[2]'
COMPANY_NAME_XPATH = '//*[@id="__layout"]/div/div[2]/section[1]/div/div/div[4]/div[1]/div[1]/div[2]/p[2]'

class CasaDosDados:
    def __init__(self) -> None:
        self._driver = None
        self.path_to_filters = None      
        # self.last_internal_url = None

    def execute(self):
       file_with_internal_urls = self.search_internal_urls()
       self.generate_file_internal_data(file_with_internal_urls)
    
    def search_internal_urls(self):
        """ Método que gera um arquivo com as urls internas """


        filters_json = self._read_json(self.path_to_filters)

        if not filters_json['cnaes'] or not filters_json['states'] or not filters_json['cities']:
            LOGGER.error(f"Necessário ter valor em todos os filtros: {filters_json}")
            exit(0)

        self._get_session()

        try:
            
            LOGGER.info(f"acessando url {SITE_URL}")
            self._driver.get(SITE_URL)
            
            LOGGER.info("maximizando")
            self._driver.maximize_window()

            LOGGER.info(f"Aplicando CNAES")
            self._apply_cnaes_filter(filters_json['cnaes'])            
            
            LOGGER.info(f"Aplicando STATES")
            self._apply_states_filter(filters_json['states'])
            
            LOGGER.info(f"Aplicando CITIES")
            self._apply_cities_filter(filters_json['cities'])
            
            btn_search = self._driver.find_element(By.XPATH, BUTTON_SEARCH_XPATH)            

            LOGGER.info("scroll to btn")            
            self._driver.execute_script("arguments[0].scrollIntoView();", btn_search)
            
            
            LOGGER.info(f"Clicando em pesquisar ...")
            btn_search.click()

            time.sleep(5)
            LOGGER.info(f"Pegando total de resultados")
            elm_total = self._driver.find_element(By.XPATH, TOTAL_RESULTS_XPATH)
            total = elm_total.text
            total = int(''.join(i for i in total if i.isdigit()))
            LOGGER.info(f"Total de resultados {total}")

            file_with_internal_urls = self._generate_file_with_internal_urls(total)
            LOGGER.info(f"path com as urls internas {file_with_internal_urls}")
            return file_with_internal_urls

        except Exception as ex:
            LOGGER.exception(f"erro {str(ex)}")
        finally:
            self._driver.quit()

    def generate_file_internal_data(self, path_to_internal_url, last_internal_url=None):
        """ Método que gera o arquivo com os dados da url interna"""

        data_list = []
        try:

            df = pd.read_csv(path_to_internal_url, sep=";")
            total = len(df)

            LOGGER.info(f"total de urls {total}")

            cont = 0
            filename = f'/tmp/data_{datetime.now().strftime("%Y%m%d")}.csv'

            for index, row in df.iterrows():
                LOGGER.info(f"{cont} de {total} - {filename}")
                LOGGER.info("fechando sessão atual caso exista")
                url = row[0]

                # se tiver last_internal_url skipa todas ate chegar nela novamente, assim continua de onde parou
                if last_internal_url:
                    cont += 1
                    if url != last_internal_url:
                        continue
                    last_internal_url = None
                    continue


                # sempre cria nova sessão para nao ser barrado pela cloudflare
                if isinstance(self._driver, object):
                    self._driver.quit()

                self._get_session()

                LOGGER.info(f"acessando url {url}")
                self._driver.get(url)
                
                cnpj = self._driver.find_element(By.XPATH, CNPJ_XPATH).text
                fantasy_name = self._driver.find_element(By.XPATH, FANTASY_NAME_XPATH).text
                if fantasy_name == 'MATRIZ':
                    fantasy_name = self._driver.find_element(By.XPATH, COMPANY_NAME_XPATH).text

                data = {
                    "cnpj": cnpj,
                    "fantasy_name": fantasy_name
                }
                data_list.append(data)
                df_data = pd.DataFrame(data_list)

                # incrementa o arquivo caso exista, assim se der erro, nao perde oq ja conseguiu
                if not os.path.isfile(filename):
                    df_data.to_csv(filename, sep=";", index=False)
                else: # else it exists so append without writing the header
                    df_data.to_csv(filename, sep=";", index=False, mode='a', header=False)

                data_list = []
                cont +=1

            return filename

        except Exception as ex:
            LOGGER.error(f"erro ao busca interno: {str(ex)}")
        finally:
            self._driver.quit()

    def _get_session(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        self._driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def _read_json(self, filepath):
        with open(filepath) as json_file:
            return json.load(json_file)

    def _apply_cnaes_filter(self, filters):
        elm = self._driver.find_element(By.XPATH, CNAE_INPUT_XPATH)
        for fill in filters:
            elm.send_keys(fill)
            elm.send_keys(Keys.ARROW_DOWN)
            elm.send_keys(Keys.RETURN)
            elm.send_keys(Keys.ESCAPE)
            LOGGER.info(f"filter cnae '{fill}' aplicado")

    def _apply_states_filter(self, filters):
        elm = self._driver.find_element(By.XPATH, STATE_INPUT_XPATH)
        for fill in filters:
            elm.send_keys(fill)
            elm.send_keys(Keys.ARROW_DOWN)
            elm.send_keys(Keys.RETURN)
            elm.send_keys(Keys.ESCAPE)
            LOGGER.info(f"filter state '{fill}' aplicado")

    def _apply_cities_filter(self, filters):
        elm = self._driver.find_element(By.XPATH, CITY_INPUT_XPATH)
        for fill in filters:
            elm.send_keys(fill)
            elm.send_keys(Keys.ARROW_DOWN)
            elm.send_keys(Keys.RETURN)
            elm.send_keys(Keys.ESCAPE)
            LOGGER.info(f"filter city '{fill}' aplicado")
    
    def _go_to_next_page(self):
        elm = self._driver.find_element(By.XPATH, BUTTON_NEXT_PAGE_XPATH)            
        elm.click()

    def _generate_file_with_internal_urls(self, total_results):
            internal_link = []
            page = 1
            while(len(internal_link) <= total_results-1):
                links = self._driver.find_elements(By.XPATH, LINKS_AFTER_FILTER_XPATH)
                for link in links:
                   internal_link.append(link.get_attribute('href'))
                
                LOGGER.info(f"[pagina atual {page}][total de links {len(internal_link)}]")
                page+=1
                try:
                    LOGGER.info(f"indo para página {page}")
                    self._go_to_next_page()
                    time.sleep(5)
                except Exception as ex:
                    LOGGER.info(f"Problema ao ir para próxima pagina {page}: {str(ex)}")
                    break
                
            LOGGER.info(f"Correu {page} paginas")
            LOGGER.info(f"Encontrou {len(internal_link)} de {total_results}")
            LOGGER.info(f"Salvando links")
            filename = f'/tmp/internal_link_{datetime.now().strftime("%Y%m%d%H%M")}.csv'
            df = pd.DataFrame(internal_link)
            df.to_csv(filename, sep=";", index=False, header=False)
            return filename