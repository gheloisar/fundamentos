import os
from bs4 import BeautifulSoup
import httpx 
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService # webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager # webdriver_manager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def acessar_pagina(link):
    pagina = httpx.get(link)
    bs = BeautifulSoup(pagina.text, "html.parser")
    return(bs)

def acessar_pagina_dinamica(link, navegador = 'chrome', tempo_espera = 10):
    if navegador == "chrome":
        pagina = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif navegador == "edge":
        pagina = webdriver.Edge(EdgeChromiumDriverManager().install())


    pagina.get(link)
    sleep(tempo_espera)
    return pagina

def encontrar_botao(pagina, xpath, diretorio_e_nome_arquivo):
    contador = 1
    while True:
        try:
            print("clique_botao")
            botao = WebDriverWait(pagina, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            botao.click()
            diretorio_e_nome_arquivo = diretorio_e_nome_arquivo.format(contador)
            salvar_pagina(pagina, diretorio_e_nome_arquivo)
            contador+=1
            sleep(10)
        except:
            print("botão não encontrado")
            break

def salvar_pagina(pagina, diretorio_e_nome_arquivo):
    with open(diretorio_e_nome_arquivo,"w", encoding="utf-8") as arquivo:
        arquivo.write(pagina.page_source)


def webscrapping_local(dir_html):
    for html in os.listdir(dir_html):
        if html.endswith(".html"):
            dir_arquivo = os.path.join(dir_html, html)
            with open(dir_arquivo, "r", encoding="utf-8") as arquivo:
                conteudo =arquivo.read()
            bs = BeautifulSoup(conteudo, "html.parser")
            #print(bs)
            extrair_infos(bs)


def extrair_infos(bs):
    # print(pagina)
    noticias = bs.find("div", attrs={"class":"StoriesList_storiesContainer__yVALX StoriesList_stacked___F3Yo"}).find_all("div", attrs={"class":"StoryCard_container__KVQRO StoryCard_boxed__fZPBX StoryCard_vertical__0C6ha"})
    # print(noticias)
    # TODO: tentar gerar todos os htmls do clicar "Load more"
    # TODO: coletar todas as informações das notícias (Título, data, tag, subtítulo, autoria e parágrafos)
    for noticia in noticias:
        link = "https://pressroom.oecs.int"+noticia.a["href"]
        titulo = noticia.find('h2').text.strip()
        data = noticia.find('time').text.strip()
        tag = noticia.find("span", attrs={"class": "Badge_badge__YfgzN Badge_small__gt79M Badge_outline__YlUOD"}) 
        tag_texto = tag.get_text(strip=True) if tag else "Tag não encontrada"
        subtitulo = noticia.find("a", attrs={"class": "StoryCard_subtitleLink__F_bW0"}) 
        subtitulo_texto = subtitulo.get_text(strip=True) if subtitulo else "Subtítulo não encontrado"
        conteudo = acessar_pagina_dinamica(link)
        paragrafos = []

        lista_tag_p = conteudo.find_elements(By.CLASS_NAME,"styles_paragraph__GiKq6")

        for paragrafo in lista_tag_p:
            tag_p = paragrafo.text
            paragrafos.append(tag_p)

        autorias = []

        lista_autoria = conteudo.find_elements(By.CLASS_NAME,"prezly-slate-contact__name")   
        
        for autoria in lista_autoria:
            autores = autoria.text
            autorias.append(autores)

        print(link)
        print("")
        print(titulo)
        print("")
        print(data)
        print("")
        print(tag_texto)
        print("")
        print(subtitulo_texto)
        print(paragrafos)
        print(autorias)
        print("#"*8)



def webscrapping_bs(pagina):
    html_pagina = pagina.page_source
    bs = BeautifulSoup(html_pagina, "html.parser")
    return bs


def clicar_botao_01(link, xpath, navegador, tempo_espera):
    pagina = acessar_pagina_dinamica(link, navegador='chrome', tempo_espera = 3)
    botao = encontrar_botao(pagina, xpath)
    bs = webscrapping_bs(pagina)
    pagina.quit()
    return bs


def main_02():
    diretorio = "../html/oecs/"
    webscrapping_local(diretorio)



def main():
    link = "https://pressroom.oecs.int/"
    xpath = ".//span[text()='Load more']"
    diretorio_e_nome_arquivo = "../html/oecs/pagina_{:05}.html"
    pagina = acessar_pagina_dinamica(link, navegador="chrome", tempo_espera=10)
    botao = encontrar_botao(pagina, xpath, diretorio_e_nome_arquivo)
    bs = webscrapping_bs(pagina)
    pagina.quit()


if __name__=="__main__":
    # main()
    main_02()

    #https://www.youtube.com/watch?v=CR_1lxzSuHw - variável de ambiente e inserção do json