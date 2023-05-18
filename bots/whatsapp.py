import os
import random
import pandas as pd
import logging
from bots.selenium import Selenium
from bots import utils

LOGGER = logging.getLogger(__name__)

XPATH_CHECK_LOGIN = '/html/body/div[1]/div/div/div[3]/div[1]/div/div/div[2]/div'
XPATH_INVALID_URL = '/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[1]'
XPATH_BTN_SEND_MSG = '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
URL_BASE = 'https://web.whatsapp.com/'

class Whatsapp(Selenium):
    def __init__(self, path_to_report, remote_url=None) -> None:
        super().__init__(remote_url=remote_url)

        self.urls = []
        self.path_to_report = path_to_report
        self.last_url = None
    
    def execute(self):    
        self._get_session()
        self._access_url(URL_BASE)
        
        while self._check_login():
            utils.force_time_sleep(10, "Aguardando leitura qrcode")

        LOGGER.info("login esta ok")
        total = len(self.urls)
        cont_invalid = 0
        cont_sent = 0

        for index, url in enumerate(self.urls):
            if self.last_url and url != self.last_url:
                    continue
            
            self.last_url = None

            data = {
                "url": url,
                "status": 'ENVIADO'
            }

            utils.force_time_sleep(random.choice(range(1, 5)), f'[{index} de {total}] [invalidas: {cont_invalid}] [enviadas: {cont_sent}]')  
            self._access_url(url)
            if self._is_invalid():
                LOGGER.info("url invalida")
                cont_invalid +=1
                data['status'] = 'INVALIDO'
            else:
                LOGGER.info("mensagem enviada")
                cont_sent +=1
                self._send_msg()            

            df_data = pd.DataFrame([data])
            # incrementa o arquivo caso exista, assim se der erro, nao perde oq ja conseguiu
            if not os.path.isfile(self.path_to_report):
                df_data.to_csv(self.path_to_report , sep=";", index=False)
            else: # else it exists so append without writing the header
                df_data.to_csv(self.path_to_report , sep=";", index=False, mode='a', header=False)
   
    def _is_invalid(self):
        if self._wait_element_by_xpath(XPATH_INVALID_URL):            
            return True
        
        return False
    
    def _check_login(self):
        if self._wait_element_by_xpath(XPATH_CHECK_LOGIN):            
            return True        
        return False

    def _send_msg(self):
        btn = self._wait_element_by_xpath(XPATH_BTN_SEND_MSG)        
        btn.click()
