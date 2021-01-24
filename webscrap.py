from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


def extract_price_adress_rooms(soup):
  
  bairros = list()
  precos = list()
  quartos = list()

  for i in range(len(soup.select(".property-card__address"))):
    # valores 'sob consulta' serao ignorados
    try:
      preco = soup.select(".property-card__values p")[i].contents
      precos.append(preco)
      bairro = soup.select(".property-card__address")[i].contents
      bairros.append(bairro)
      quarto = soup.select(".js-property-detail-rooms span.property-card__detail-value")[i].contents
      quartos.append(quarto)
    except(IndexError):
      continue

  for i in range(len(precos)):
    precos[i] = str(precos[i][0])
    bairros[i] = str(bairros[i][0])
    quartos[i] = str(quartos[i][0])

  return precos, bairros, quartos

def montar_listas(soup):
    # go through next pages clicking with selenium
    all_precos = list()
    all_rooms = list()
    all_addresses = list()
    precos, bairros, quartos = extract_price_adress_rooms(soup)

    for preco in precos:
        all_precos.append(preco)
    for room in quartos:
        all_rooms.append(room)    
    for bairro in bairros:
        all_addresses.append(bairro)

    return all_precos, all_addresses, all_rooms

def main():

    path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get("https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/apartamento_residencial/")
    
    preco_filtrado = list()
    bairro_filtrado = list()
    quarto_filtrado = list()

    contador = 0
    for i in range(30):
        if(contador !=0):
            driver.find_element_by_xpath("//a[@title='Próxima página']").click()    
    
        element = driver.page_source
        soup = BeautifulSoup(element, "html.parser")
        precos, bairros, quartos = montar_listas(soup)
        #time.sleep(3)
        contador+=1
    
        for i in range(len(precos)):
            try:
                preco_filtrado.append(precos[i].split()[1])
                bairro_filtrado.append(bairros[i])
                quarto_filtrado.append(quartos[-1].split()[0])
            except IndexError:
                continue
                
                
    print(quartos[-1].split()[0])
    print(len(bairro_filtrado))
    print(len(preco_filtrado))
    print(len(quarto_filtrado))

    time.sleep(2)
    driver.quit()

if __name__ == '__main__':
    main()