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

    obj.links = ['https://www.google.com.br/maps/place/Rp+Borracharia/data=!4m7!3m6!1s0x94dcfdc702e7050f:0x7ee1389b0a27d5c1!8m2!3d-25.5727095!4d-49.3379463!16s%2Fg%2F11hrkrckrc!19sChIJDwXnAsf93JQRwdUnCps44X4?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Casa+De+Carnes+Boi+Dourado/data=!4m7!3m6!1s0x94dcfe759f46dcd5:0x7db556ac154431c0!8m2!3d-25.5925639!4d-49.3420446!16s%2Fg%2F11f3r103dw!19sChIJ1dxGn3X-3JQRwDFEFaxWtX0?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Camilo+Hortigranjeiros+Distribuidor+Atacadista+Ceasa/data=!4m7!3m6!1s0x94dcfc429f905a61:0xdaa35c1d4ffdd851!8m2!3d-25.5532634!4d-49.3016516!16s%2Fg%2F1tknllkl!19sChIJYVqQn0L83JQRUdj9Tx1co9o?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Nova+Esperan%C3%A7a+Materiais+de+Constru%C3%A7%C3%A3o/data=!4m7!3m6!1s0x94dcfc84ee7f16d7:0x44fd15385487d91c!8m2!3d-25.5885568!4d-49.3356639!16s%2Fg%2F1tfw45ky!19sChIJ1xZ_7oT83JQRHNmHVDgV_UQ?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/BORRACHARIA+DETROIT/data=!4m7!3m6!1s0x94dcfd67b26b933d:0x6e680cc6eddc7062!8m2!3d-25.5826256!4d-49.3370853!16s%2Fg%2F11fk48vk2n!19sChIJPZNrsmf93JQRYnDc7cYMaG4?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Dw+AutoParts+Comercio+de+Pe%C3%A7as/data=!4m7!3m6!1s0xa64153a2dd315f13:0x690f7f89fc80ce76!8m2!3d-25.5948536!4d-49.3410457!16s%2Fg%2F11sct5yyvk!19sChIJE18x3aJTQaYRds6A_Il_D2k?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Artefatos+de+Cimento+Zenko/data=!4m7!3m6!1s0x94dcfc061ba1a38f:0xd4129220183a7a03!8m2!3d-25.563746!4d-49.2884225!16s%2Fg%2F1tz72jq7!19sChIJj6OhGwb83JQRA3o6GCCSEtQ?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Kaffer+Modas/data=!4m7!3m6!1s0x94dcfdd8c25ffb69:0xf59a8fdcdf609db1!8m2!3d-25.588488!4d-49.338619!16s%2Fg%2F11c6lf8q66!19sChIJaftfwtj93JQRsZ1g39yPmvU?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Com%C3%A9rcio+de+Bebidas+Fran%C3%A7a/data=!4m7!3m6!1s0x94dcfd4af1377a9b:0x5bda9ea64518f811!8m2!3d-25.5734325!4d-49.3314108!16s%2Fg%2F11hz0kmq3q!19sChIJm3o38Ur93JQREfgYRaae2ls?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Espaco+da+Ro/data=!4m7!3m6!1s0x94dcff4416b2872f:0x3f1364e7303ea1ed!8m2!3d-25.6144819!4d-49.3419541!16s%2Fg%2F11kzcdq20k!19sChIJL4eyFkT_3JQR7aE-MOdkEz8?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Casa+Bela+Materiais+de+Contru%C3%A7%C3%A3o/data=!4m7!3m6!1s0x94dcffeaafed6cbf:0x5ff021ef6b03c782!8m2!3d-25.59248!4d-49.3401767!16s%2Fg%2F11lt3l12rn!19sChIJv2ztr-r_3JQRgscDa-8h8F8?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Borracharia/data=!4m7!3m6!1s0x94dcfc4281de8f4d:0x9cda29552a44d67b!8m2!3d-25.5514001!4d-49.304472!16s%2Fg%2F11h5km8t8f!19sChIJTY_egUL83JQRe9ZEKlUp2pw?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/gg+pe%C3%A7as+usadas+e+novas+melhor+pre%C3%A7o+da+cidade/data=!4m7!3m6!1s0x94dcfda66af97cf9:0x1d778760a470f52e!8m2!3d-25.5538889!4d-49.3363889!16s%2Fg%2F11d_wm2x4k!19sChIJ-Xz5aqb93JQRLvVwpGCHdx0?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Zaidir+G%C3%A1s/data=!4m7!3m6!1s0x94dcfdda52e182bf:0xfb3940fff2b4115d!8m2!3d-25.583056!4d-49.3372206!16s%2Fg%2F11b7rxksdd!19sChIJv4LhUtr93JQRXRG08v9AOfs?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Campo+de+Santana/data=!4m7!3m6!1s0x94dcfe67cce7bcbf:0xb04dda43c8558fd!8m2!3d-25.5919015!4d-49.3318651!16s%2Fg%2F1ymwcx4v8!19sChIJv7znzGf-3JQR_ViFPKTdBAs?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Olitintas+Com%C3%A9rcio+de+Tintas+Ltda/data=!4m7!3m6!1s0x94dcfdbb9b5f1231:0x6611296b1a2d7008!8m2!3d-25.5638016!4d-49.3390732!16s%2Fg%2F1vg4kz6q!19sChIJMRJfm7v93JQRCHAtGmspEWY?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Borracharia+BR+PNEUS/data=!4m7!3m6!1s0x94dcfe8a57a4995b:0x1fb5c79ac29608ae!8m2!3d-25.6018753!4d-49.3227118!16s%2Fg%2F11fs1nh_q7!19sChIJW5mkV4r-3JQRrgiWwprHtR8?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Mk+Com%C3%A9rcio/data=!4m7!3m6!1s0x94dce46939bef16d:0x4c1cde8198310b29!8m2!3d-14.4095262!4d-51.31668!16s%2Fg%2F1pv0wbxdt!19sChIJbfG-OWnk3JQRKQsxmIHeHEw?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Alcino+Almeida+-+Erva+e+Plantas/data=!4m7!3m6!1s0x94dcff235841a285:0x129112ebb72cde4c!8m2!3d-25.604598!4d-49.3277811!16s%2Fg%2F11k39gmpl8!19sChIJhaJBWCP_3JQRTN4st-sSkRI?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Medeiros+Materiais+El%C3%A9tricos/data=!4m7!3m6!1s0x94dcfdc41fb7203f:0x8cef08a21952a45b!8m2!3d-25.5624202!4d-49.3391563!16s%2Fg%2F1ptwlqgzc!19sChIJPyC3H8T93JQRW6RSGaII74w?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Super+Eli+Mais+Tatuquara/data=!4m7!3m6!1s0x94dcfdf986001919:0xfae491e78df2b600!8m2!3d-25.5763568!4d-49.3350405!16s%2Fg%2F11sgzykqmc!19sChIJGRkAhvn93JQRALbyjeeR5Po?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/D%27marka+Outlet/data=!4m7!3m6!1s0x94dcff41328f05d3:0xe52ca7d06f7552e1!8m2!3d-25.5596888!4d-49.331566!16s%2Fg%2F11hztd0w41!19sChIJ0wWPMkH_3JQR4VJ1b9CnLOU?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/E.J.S+Materiais+de+Constru%C3%A7%C3%A3o/data=!4m7!3m6!1s0x94dcfdb1eda2c057:0x1c3481d0482c8ec7!8m2!3d-25.5591587!4d-49.330497!16s%2Fg%2F11cjmb2j7y!19sChIJV8Ci7bH93JQRx44sSNCBNBw?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Pneuflex+Recauchutagem+de+Pneus/data=!4m7!3m6!1s0x94dcfc44954fb805:0x82729d25a0911308!8m2!3d-25.5539106!4d-49.3097444!16s%2Fg%2F1wbryyk5!19sChIJBbhPlUT83JQRCBORoCWdcoI?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Supermercado+Wozniak/data=!4m7!3m6!1s0x94dcfddf19a2109f:0x53873559627adb94!8m2!3d-25.5892024!4d-49.3415145!16s%2Fg%2F11b7q55kzd!19sChIJnxCiGd_93JQRlNt6Ylk1h1M?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Pneutek+-+Com%C3%A9rcio+de+C%C3%A2maras+de+Ar/data=!4m7!3m6!1s0x94dcfc850fc17fe1:0x4afbb5fe08288c8b!8m2!3d-25.6042384!4d-49.31554!16s%2Fg%2F11b5pj3qbn!19sChIJ4X_BD4X83JQRi4woCP61-0o?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Com%C3%A9rcio+de+bebidas+MK/data=!4m7!3m6!1s0x94dcfd65dd1db283:0x19ba709212271059!8m2!3d-25.5623062!4d-49.3327233!16s%2Fg%2F11gnbd5dlw!19sChIJg7Id3WX93JQRWRAnEpJwuhk?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Visocool/data=!4m7!3m6!1s0x94dcfdba5741a84b:0x6cbb99a07c3c57fe!8m2!3d-25.5629618!4d-49.3368283!16s%2Fg%2F11f3r1lmbv!19sChIJS6hBV7r93JQR_lc8fKCZu2w?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/TCA+Materiais+para+Constru%C3%A7%C3%A3o/data=!4m7!3m6!1s0x94dcfe83b350befd:0xbb449572ecb67205!8m2!3d-25.5858076!4d-49.3180961!16s%2Fg%2F1tflz0wf!19sChIJ_b5Qs4P-3JQRBXK27HKVRLs?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Com%C3%A9rcio+de+Colch%C3%B5es+Bilek+Parazzi/data=!4m7!3m6!1s0x94dcfdb03b9b821b:0xebd806dbf78b2dc1!8m2!3d-25.5599016!4d-49.3332214!16s%2Fg%2F1ptxgfmn3!19sChIJG4KbO7D93JQRwS2L99sG2Os?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/DISTRIBUI%C3%87%C3%83O+DE+PNEUS+AGRICOLAS/data=!4m7!3m6!1s0x94dcfde340a2d219:0xc56740bfbfaac038!8m2!3d-25.6040703!4d-49.3153661!16s%2Fg%2F11rj44ybg2!19sChIJGdKiQOP93JQROMCqv79AZ8U?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Alan+Car+Som+e+Acess%C3%B3rios/data=!4m7!3m6!1s0x94dcfdc87a52c169:0x90296664a1e0dedd!8m2!3d-25.5711831!4d-49.3344238!16s%2Fg%2F11hbkj0_sf!19sChIJacFSesj93JQR3d7goWRmKZA?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Avi%C3%A1rio+fam%C3%ADlia/data=!4m7!3m6!1s0x94dcfda2b5db8999:0x3b32a5f107dc07db!8m2!3d-25.5651448!4d-49.3359027!16s%2Fg%2F11t2znt181!19sChIJmYnbtaL93JQR2wfcB_GlMjs?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Aviario+Calopsita/data=!4m7!3m6!1s0x94dcfdd8e81eed1b:0xa1cf772393e06f36!8m2!3d-25.5884309!4d-49.3386549!16s%2Fg%2F11gf0vz4gs!19sChIJG-0e6Nj93JQRNm_gkyN3z6E?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Dalla+g%C3%A1s/data=!4m7!3m6!1s0x94dcfd21075436cd:0xeb9f6085eb172e31!8m2!3d-25.5597022!4d-49.3186311!16s%2Fg%2F11rp33q54g!19sChIJzTZUByH93JQRMS4X64Vgn-s?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Atz+Pneus+-+Recapadora/data=!4m7!3m6!1s0x94db24c5f1f594dd:0x559c8040f595664a!8m2!3d-25.5845974!4d-49.3145238!16s%2Fg%2F1w04l7kk!19sChIJ3ZT18cUk25QRSmaV9UCAnFU?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/VIP+MERCEARIA+E+BEBIDAS/data=!4m7!3m6!1s0x94dcfdbaa80c5955:0x3c24ebe6f9528faa!8m2!3d-25.5595608!4d-49.331426!16s%2Fg%2F11r3dz9g5w!19sChIJVVkMqLr93JQRqo9S-ebrJDw?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Costy+Com%C3%A9rcio+de+Confec%C3%A7%C3%B5es/data=!4m7!3m6!1s0x94dcfdbb4fd4bc61:0x98932ef9313749d!8m2!3d-25.5613444!4d-49.3391678!16s%2Fg%2F1ptz9fg5t!19sChIJYbzUT7v93JQRnXQTk-8yiQk?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Dom+Bosco+Borracharia/data=!4m7!3m6!1s0x94dcfe81af31bb77:0x1616b498783f5042!8m2!3d-25.5867321!4d-49.3216135!16s%2Fg%2F11cn7kd0tf!19sChIJd7sxr4H-3JQRQlA_eJi0FhY?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/UPA+Comercio+de+Bebidas+e+Conveni%C3%AAncia/data=!4m7!3m6!1s0x94dcfdb37f828805:0xc7e4b083a9c3b36!8m2!3d-25.5780923!4d-49.3375857!16s%2Fg%2F11s7y4sz6q!19sChIJBYiCf7P93JQRNjucOghLfgw?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Charsav+Com%C3%A9rcio+de+Medicamentos+e+Perfumaria/data=!4m7!3m6!1s0x94dcfdd8a42e5973:0x5076c90d25a25c8c!8m2!3d-25.5900599!4d-49.3390246!16s%2Fg%2F1ptwb9b13!19sChIJc1kupNj93JQRjFyiJQ3JdlA?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Armaz%C3%A9m+da+Fam%C3%ADlia+Campo+do+Santana/data=!4m7!3m6!1s0x94dcfe840a2c2ba1:0x321b740585eb9793!8m2!3d-25.5883604!4d-49.31836!16s%2Fg%2F1td6tcvn!19sChIJoSssCoT-3JQRk5frhQV0GzI?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Da%27sambel+comercio+de+bebidas/data=!4m7!3m6!1s0x94dcfd4e8affb10d:0x1a9c1b6c027e467d!8m2!3d-25.5563915!4d-49.3243064!16s%2Fg%2F11n2q0_6_7!19sChIJDbH_ik793JQRfUZ-AmwbnBo?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Borracharia+Moraes/data=!4m7!3m6!1s0x94dcfddbadb80871:0x6e0dbac575f8b3f0!8m2!3d-25.5830372!4d-49.3376701!16s%2Fg%2F11qlzyxz14!19sChIJcQi4rdv93JQR8LP4dcW6DW4?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Futuragro+Distribuidora+de+Insumos+Agr%C3%ADcolas/data=!4m7!3m6!1s0x94dcfc69a76d427d:0xb4d8e6e3b0bfec7d!8m2!3d-25.563376!4d-49.308727!16s%2Fg%2F11b7l45qnk!19sChIJfUJtp2n83JQRfey_sOPm2LQ?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/BK+Com%C3%A9rcio+de+Madeiras/data=!4m7!3m6!1s0x94dcfd2b12367025:0xc32e6f81c76d6627!8m2!3d-25.5901581!4d-49.3441163!16s%2Fg%2F11tbttpj54!19sChIJJXA2Eiv93JQRJ2Ztx4FvLsM?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Bragante+informatica/data=!4m7!3m6!1s0x94dcfda52bc9d1df:0x2339ee74635cabe4!8m2!3d-25.5602795!4d-49.3373291!16s%2Fg%2F11dynccqpf!19sChIJ39HJK6X93JQR5KtcY3TuOSM?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/F+Aguiar+Com%C3%A9rcio+de+Medicamentos/data=!4m7!3m6!1s0x94dcfdd9190979bb:0x86c4956b74aabd6c!8m2!3d-25.5873301!4d-49.338866!16s%2Fg%2F1ptvxn9d2!19sChIJu3kJGdn93JQRbL2qdGuVxIY?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Alaska+Bebidas+e+Tabacaria/data=!4m7!3m6!1s0x94dcfe770a7607e3:0xdeef7268813f8244!8m2!3d-25.5936013!4d-49.3369982!16s%2Fg%2F11c0t8z_w1!19sChIJ4wd2Cnf-3JQRRII_gWhy794?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Ivai+Materiais+De+Constru%C3%A7%C3%A3o/data=!4m7!3m6!1s0x94dcfdb69905af81:0xecea1f64c5cfa91c!8m2!3d-25.5642854!4d-49.330268!16s%2Fg%2F11f1krg_v5!19sChIJga8Fmbb93JQRHKnPxWQf6uw?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Idealfix+-+Parafusos+e+Fixadores/data=!4m7!3m6!1s0x94dcfdf0599ac0ed:0x5e59b52147e429be!8m2!3d-25.5515437!4d-49.3386326!16s%2Fg%2F11ng6yjbj8!19sChIJ7cCaWfD93JQRvinkRyG1WV4?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Doce465/data=!4m7!3m6!1s0x94dcfdcff3cdbac1:0x8a7bf2959cf093f1!8m2!3d-25.5633909!4d-49.313202!16s%2Fg%2F11fn8q536k!19sChIJwbrN88_93JQR8ZPwnJXye4o?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Paris+Perfumaria+%26+Cosm%C3%A9ticos/data=!4m7!3m6!1s0x94dcfd069b098841:0x44744fca47600da0!8m2!3d-25.5635739!4d-49.3390964!16s%2Fg%2F11l4hdgmbw!19sChIJQYgJmwb93JQRoA1gR8pPdEQ?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/TinTin+Casa+de+Frios/data=!4m7!3m6!1s0x94dcfda3a0953a61:0x330baa2b49afb408!8m2!3d-25.5607963!4d-49.3393479!16s%2Fg%2F11rr8d0yhp!19sChIJYTqVoKP93JQRCLSvSSuqCzM?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Loja+Evang%C3%A9lica/data=!4m7!3m6!1s0x94dcff752c1a9c19:0x58cfa1a2c9d74573!8m2!3d-25.5908019!4d-49.3396582!16s%2Fg%2F11grc14fs7!19sChIJGZwaLHX_3JQRc0XXyaKhz1g?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Bazar+Avenida/data=!4m7!3m6!1s0x94dcff67602777e9:0xf95e915d9cbb29dd!8m2!3d-25.590942!4d-49.3396914!16s%2Fg%2F11gxrw9lpc!19sChIJ6XcnYGf_3JQR3Sm7nF2RXvk?authuser=0&hl=pt-BR&rclk=1',
 'https://www.google.com.br/maps/place/Ej+Lima+Borracharia+E+Lava+Car/data=!4m7!3m6!1s0x94dcfddaa0bb65fb:0xf8e7f377c163d653!8m2!3d-25.5800697!4d-49.3348338!16s%2Fg%2F11kdtj3c_9!19sChIJ-2W7oNr93JQRU9ZjwXfz5_g?authuser=0&hl=pt-BR&rclk=1'
]
    obj.execute()

if __name__ == "__main__":
    fire.Fire()