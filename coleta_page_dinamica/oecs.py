from bs4 import BeautifulSoup
from coleta_dinamica import *

def extrair_infos(bs):
    noticias = bs.find_all('div', attrs={'class':'StoryCard_container__KVQRO StoryCard_boxed__fZPBX StoryCard_vertical__0C6ha'})
    for noticia in noticias:
        link = noticia.a['href']
        print(link)

def main():
    link = 'https://pressroom.oecs.int/'
    #/html/body/div[1]/main/div[1]/button
    xpath = '/html/body/div[1]/main/div[1]/button'
    bs = clicar_botao_01(link=link, xpath=xpath, navegador='chrome', tempo_espera= 10)
    extrair = extrair_infos(bs)



if __name__=="__main__":
    main()
