import fire
import logging
import sys

console = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(format='[%(asctime)s] %(name)s %(levelname)s: %(message)s', level=logging.INFO, handlers=[console])
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

def get_data_by_google_maps(path_to_companies=None, last_cnpj=None):
    
    from bots.google import GetDataByGoogleMaps
    obj = GetDataByGoogleMaps()    
    obj.path_to_companies = path_to_companies
    obj.last_cpf_cnpj = last_cnpj
    obj.execute()

if __name__ == "__main__":
    fire.Fire()