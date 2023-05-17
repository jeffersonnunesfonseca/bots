import re
import json
import logging
import time
from unidecode import unidecode

LOGGER = logging.getLogger(__name__)

def only_numbers(string: str):
    if not string:
        return None
    
    return int(''.join(i for i in string if i.isdigit()))

def force_time_sleep(seconds: int, msg: str=None):
    LOGGER.info(f"{msg}: aguarda {seconds} segundos ...")
    cont = 0
    while cont < seconds:
        time.sleep(1)
        cont +=1

def string_to_url(string: str, sep="+"):
    string = unidecode(string)
    return string.replace(" ", sep).lower()

def pretty_json(data):
    return json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True)

def is_site(str):
    """ diz se é um site """

    # Regex to check valid URL
    regex = ("((http|https)://)?(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
     
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty
    # return false
    if (str == None):
        return False
 
    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True

    return False

def has_cep(str):
    regex = "[0-9]{5}-[\d]{3}"
    p = re.compile(regex)
    if not str:
        return False
    
    if(re.search(p, str)):
        return True
        
    return False

def is_cellphone(cellphone: str):
    CELLPHONE_RE = re.compile(r'\b\d{2}[6789]\d*\b')
    return CELLPHONE_RE.match(cellphone)