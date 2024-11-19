from bs4 import BeautifulSoup
from coleta_dinamica import *

def extrair_infos(bs):
    pass



def main():
    link = 'https://pressroom.oecs.int/'
    #/html/body/div[1]/main/div[1]/button
    xpath = '/html/body/div[1]/main/div[1]/button'
    bs = clicar_botao_01(link=link, xpath=xpath)
    extrair = extrair_infos(bs)



if __name__=="__main__":
    main()
