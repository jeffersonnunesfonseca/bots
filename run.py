import fire
import logging
import sys
from datetime import datetime
console = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(f"./logs/{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
LOGGER = logging.getLogger(__name__)

def get_data_casa_dos_dados(path_to_filters=None, path_to_internals_url=None, skip_get_internal_url=False, last_internal_url=None):
    """
    path_to_filters(str): caminho com arquivo padrão de filtros, olhar estrutura no readme
    path_to_internals_url(str): caminho para o arquivo de urls internas
    skip_get_internal_url(bool): determina se vai rodar o step de pegar urls internas
    last_internal_url(str): continua a pegar dados interno após essa url
    """
    
    from bots.casa_dos_dados import CasaDosDados
    obj = CasaDosDados()    
    obj.path_to_filters = path_to_filters
    if skip_get_internal_url:
        obj.generate_file_internal_data(path_to_internals_url, last_internal_url)
    else:
        obj.execute()

def get_data_by_google_maps(path_to_companies=None, last_cnpj=None, only_celphone=True):
    
    from bots.google import GetDataByGoogleMaps
    obj = GetDataByGoogleMaps()    
    obj.path_to_companies = path_to_companies
    obj.last_cpf_cnpj = last_cnpj
    obj.only_cellphone = only_celphone
    obj.execute()

def get_data_google_maps_by_term(term: str, path_to_save: str):
    
    from bots.google import GetDataGoogleMapsByTerm
    remote_url = "http://127.0.0.1:4444/wd/hub"
    obj = GetDataGoogleMapsByTerm(term, path_to_save, remote_url)    


    obj.execute()

if __name__ == "__main__":
    fire.Fire()