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

# Bot para coletar dados Google Maps baseado na planilha gerada pela casa dos dados

## Obs:
- todos arquivos gerados serão salvos em `/tmp`
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


# Bot para coletar dados Google Maps baseado em um termo de pesquisa

## Obs:
 - Você irá passar um termo e o bot irá coletar informações de todas as empresas localizadas na busca
## Requerimentos:
 - saber o termo a ser buscado e uma caminho onde será salvo os dados
### Explicação:
    -   para rodar basta executar: 
    ```
    python run.py get_data_google_maps_by_term '<term>' '<path_to_save> <remote_url>'
                            termo a ser buscado /\
                            lugar onde seá salvo o resultado /\
                                                url servidor selenium se tiver /\

    ```
    - Exemplo real:
    ```
        python run.py get_data_google_maps_by_term 'comércios em santa rita curitiba' '/home/jefferson/Documentos/lead/' 'http://127.0.0.1:4444/wd/hub'
    ```


# Bot para envio de mensagem no whatsapp

## Obs:
 - Bot pega uma lista de telefones e uma lista com mensagens e começa a enviar, necessário realizar a leitura do qrcode, a ideia da lista de mensagens é para não enviar sempre a mesma para que o whats nao bloqueie.
## Requerimentos: 
 - Você irá passar um caminho de um `.csv` com os numeros de telefone e um outro `.csv` com as mensagens, no momento ainda sem parametros, importante a msg deve estar encodada no padrão de url, pode utilizar esse (site)[https://www.urlencoder.org/]
 separador será `;`
### Explicação:
    -   para rodar basta executar: 
    ```
    python run.py send_whatsapp '<phone_path>' '<msg_path>' '<report_path>' '<remote_url>'
    caminho do arquivo com os telefones /\
            caminho do arquivo com as mensagens /\
                            caminho onde será salvo os relatórios /\
                                                url servidor selenium se tiver /\


    ```
    - Exemplo real:
    ```
        python run.py send_whatsapp '/home/jefferson/Documentos/phones.csv' '/home/jefferson/Documentos/messages.csv' '/home/jefferson/Documentos/reports.csv' 'http://127.0.0.1:4444/wd/hub'
    ```

- layout do `telefones.csv`:
```
phone
41997668808
41997308146
```

- layout do `msgs.csv`:
```
message
Ol%C3%A1%2C%20te%20encontrei%20no%20Google%21%0A%0ASou%20Jefferson%20Nunes%20Fonseca%2C%20especialista%20em%20solu%C3%A7%C3%B5es%20tecnol%C3%B3gicas.%20Estou%20validando%20uma%20ideia%20para%20criar%20meu%20pr%C3%B3prio%20neg%C3%B3cio%20e%20gostaria%20da%20sua%20opini%C3%A3o.%0A%0APoderia%20responder%20a%20algumas%20perguntas%20r%C3%A1pidas%3F%20Criei%20um%20formul%C3%A1rio%20no%20Google%20Forms%20para%20entender%20melhor%20as%20necessidades%20e%20desafios%20enfrentados%20por%20profissionais%20como%20voc%C3%AA.%0A%0ALevar%C3%A1%20menos%20de%201%20minuto%20do%20seu%20tempo.%20Acesse%20o%20formul%C3%A1rio%20aqui%3A%20https%3A%2F%2Fforms.gle%2FY17vZAshHwNjBpAz5.%0A%0ASua%20contribui%C3%A7%C3%A3o%20ser%C3%A1%20muito%20valiosa%20para%20moldar%20meu%20projeto.%20Agrade%C3%A7o%20antecipadamente%21%0A%0AAtenciosamente%2C%0A%0AJefferson%20Nunes%20Fonseca
Ol%C3%A1%2C%20me%20chamo%20Jefferson%20Fonseca%20e%20te%20encontrei%20no%20Google%21%0A%0ASou%20especialista%20em%20solu%C3%A7%C3%B5es%20tecnol%C3%B3gicas.%20Estou%20validando%20uma%20ideia%20para%20criar%20meu%20pr%C3%B3prio%20neg%C3%B3cio%20e%20gostaria%20da%20sua%20opini%C3%A3o.%0A%0ALevar%C3%A1%20menos%20de%201%20minuto%20do%20seu%20tempo.%20Acesse%20o%20formul%C3%A1rio%20aqui%3A%20https%3A%2F%2Fforms.gle%2FY17vZAshHwNjBpAz5.%0A%0ASua%20contribui%C3%A7%C3%A3o%20ser%C3%A1%20muito%20valiosa%20para%20moldar%20meu%20projeto.%20Agrade%C3%A7o%20antecipadamente%21


```
# SUBIR SELENIUM SERVER
```
sh run_selenium_server.sh
```