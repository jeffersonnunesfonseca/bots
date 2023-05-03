# Python versão 3.10
- O objetivo desse projeto é deixar de maneira agrupada e organizada todos os tipo de bots que geralmente utilizo.


- instalar pacotes
```
pip install -r requirements.txt
```

# Bot para casa dos dados
## Requerimentos:
- ter um arquivo json de filtros seguindo o seguinte padrão:
```
{
    "cnaes": [
        "5250801"
    ],
    "states": [
        "SÃO PAULO",
        "RIO DE JANEIRO",
        "PARANA"
    ],
    "cities": [
        "CURITIBA",
        "SÃO PAULO",
        "RIO DE JANEIRO"

    ]
}
```

## Como executar
- para rodar deve ter em mãos o caminho do arquivo de filtros e rodar o seguinte comando:
```
python run.py get_data_casa_dos_dados '<path_to_filter>.json'
```
- caso ja tenha o arquivo com as urls basta rodar o seguinte comando, passando o arquivo das urls:
```
python run.py get_data_casa_dos_dados None '<path_to_internal_links>' True '<last_internal_url>'
                       path_to_filters /\
                                path_to_internal_links /\
                                       ignore get internal links step? /\
                                              continue after this url? else set None /\
                                       
```

### Explicação:
- o comando acima irá acessar o site da casa dos dados, aplicar os filtros disponiveis e pegar as urls internas, após isso, o robo irá acessar url por url pegando as info necessárias e salvar no '/tmp/data_YYYYMMDDHHMM.csv'
- o arquivo estará em csv separado por ';', abaixo o template atual
```
cnpj;fantasy_name
36.954.487/0001-99;HEALTH MEDICAL

```

# Bot para coletar dados Google Maps

## Requerimentos:
- ter um arquivo csv no seguinte padrão (obs: o robô da casa dos dados irá gerar esse arquivo):
```
cnpj;fantasy_name
36.954.487/0001-99;HEALTH MEDICAL
```
## Como executar
- Basta rodar o seguinte comando:
```
python run.py get_data_by_google_maps '/tmp/data_20230502.csv' None
```
- Caso queira continuar após um cnpj x, rodar dessa forma:
```
python run.py get_data_by_google_maps '/tmp/data_20230502.csv' 'cnpjx'
                                caminho do arquivo /\
                                            continuar após cnpj /\     
```



### Explicação:
- Bot irá tentar encontrar algumas informações no bloco de dados que o google maps trás quando acerta a busca(endereço, site, telefone),se nao tiver o telefone é considerado que não encontrou.
- será gerado dois arquivos, `lead_YYYYMMDD.csv` que irá conter os cnpjs com contato encontrado e um outro chamado `not_found_lead_YYYYMMDD.csv` que irá conter os que não foram encontrados. 

- layout do `lead_YYYYMMDD.csv`:
```
fantasy_name;cnpj;address;site;phone
VR CONSULT LTDA;41.640.274/0001-22;Rua Pais de Araújo, 29 - Cobertura - Itaim Bibi, São Paulo -
```
- layout do `not_found_lead_YYYYMMDD.csv`:
```
fantasy_name;cnpj;exception
HEALTH MEDICAL;36.954.487/0001-99;block 1 not found
```