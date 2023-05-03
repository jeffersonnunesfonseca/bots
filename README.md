# Python versão 3.10
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

https://casadosdados.com.br/solucao/cnpj/acl-comissaria-de-despachos-aduaneiros-ltda-66614702000173