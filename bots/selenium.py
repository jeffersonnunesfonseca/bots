import logging
import time
import random
import platform

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import exceptions as selenium_ex
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

from bots import utils

LOGGER = logging.getLogger(__name__)

class Selenium:
    def __init__(self, remote_url=None) -> None:
        self._driver = None
        self.remote_url = remote_url

    def _get_session(self):
        options = webdriver.ChromeOptions()
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])
        options.add_argument('--ignore-certificate-errors')   
        if self.remote_url:
            self._driver = webdriver.Remote(options=options, command_executor=self.remote_url)   
        else:
            self._driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self._driver.maximize_window()

    def _access_url(self, url):
        self._driver.get(url)
        utils.force_time_sleep(10, f"acessando url {url}")
    
    def _wait_element_by_xpath(self, xpath: str, wait_time: int = 30):
        """ retorna o elemento apenas quando é carregado """

        try:
            wait =  WebDriverWait(self._driver, wait_time)
            return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))   
            
        except selenium_ex.TimeoutException as ex:
            return False
        
    def _wait_elements_by_xpath(self, xpath: str, wait_time: int = 30):
        """ retorna o elemento apenas quando é carregado """
        
        try:
            wait =  WebDriverWait(self._driver, wait_time)
            return wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))   
          
        except selenium_ex.TimeoutException as ex:
            return False