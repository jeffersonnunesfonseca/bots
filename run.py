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

def send_whatsapp():
    path_to_report = '/home/jefferson/Documentos/reports.csv'
    remote_url = "http://127.0.0.1:4444/wd/hub"
    urls = ['https://web.whatsapp.com/send/?phone=5541997668808&text=Ol%C3%A1,%20te%20encontrei%20no%20Google!%0A%0ASou%20Jefferson%20Fonseca,%20especialista%20em%20solu%C3%A7%C3%B5es%20tecnol%C3%B3gicas.%20Estou%20validando%20uma%20ideia%20para%20criar%20meu%20pr%C3%B3prio%20neg%C3%B3cio%20e%20gostaria%20da%20sua%20opini%C3%A3o.%0A%0APoderia%20responder%20a%20algumas%20perguntas%20r%C3%A1pidas?%20Criei%20um%20formul%C3%A1rio%20no%20Google%20Forms%20para%20entender%20melhor%20as%20necessidades%20e%20desafios%20enfrentados%20por%20profissionais%20como%20voc%C3%AA.%0A%0ALevar%C3%A1%20menos%20de%201%20minuto%20do%20seu%20tempo.%20Acesse%20o%20formul%C3%A1rio%20aqui:%20https://forms.gle/Y17vZAshHwNjBpAz5.%0A%0ASua%20contribui%C3%A7%C3%A3o%20ser%C3%A1%20muito%20valiosa%20para%20moldar%20meu%20projeto.%20Agrade%C3%A7o%20antecipadamente!%0A%0AAtenciosamente,%0A%0AJefferson%20Fonseca']
    
    from bots.whatsapp import Whatsapp
    bot = Whatsapp(path_to_report, remote_url)
    bot.urls = urls
    bot.execute()
    
if __name__ == "__main__":
    fire.Fire()