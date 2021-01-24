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
            preco = soup.select(".property-card__content div.property-card__price p")[i].contents
            precos.append(preco)
            bairro = soup.select(".property-card__address")[i].contents
            bairros.append(bairro)
            quarto = soup.select(".js-property-detail-rooms span.property-card__detail-value")[i].contents
            quartos.append(quarto)
        except(IndexError):
            continue
    
    for i in range(len(precos)):
        try:
            precos[i] = float(str(precos[i][0].split()[1].replace('.','')))
            bairros[i] = str(bairros[i][0])
            quartos[i] = str(quartos[i][0].split()[0])
        except IndexError:
            continue

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

def clean_dataframe(dataframe):
    
    indexRemove = dataframe[dataframe['precos'] == list ].index
    dataframe.drop(indexRemove , inplace=True)
    
    indexRemove = dataframe[dataframe['bairros'] == list ].index
    dataframe.drop(indexRemove , inplace=True)
    
    indexRemove = dataframe[dataframe['quartos'] == list ].index
    dataframe.drop(indexRemove , inplace=True)

    # it's necessary remove values below 5000 reais because this values is associated with rent not sales
    indexRemove = dataframe[dataframe['precos'] < 5000 ].index
    # Delete these row indexes from dataFrame
    dataframe.drop(indexRemove , inplace=True)
    dataframe.to_csv('imoveis.csv')

def create_dataframe(bairro, quartos, precos):
    
    df = pd.DataFrame()
    df["bairros"] = bairro
    df["quartos"] = quartos
    df["precos"] = precos
    clean_dataframe(df)

def main():

    path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get("https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/apartamento_residencial/")
    
    preco_filtrado = list()
    bairro_filtrado = list()
    quarto_filtrado = list()

    counter = 0
    for i in range(179):
        #if(counter):
        time.sleep(.5)
        element = driver.page_source
        soup = BeautifulSoup(element, "html.parser")
        precos, bairros, quartos = montar_listas(soup)
        counter+=1
        print('--------- counter {}'.format(counter))
        for j in range(len(precos)):
            try:
                #preco_filtrado.append(precos[i].split()[1])
                preco_filtrado.append(precos[j])
                bairro_filtrado.append(bairros[j])
                quarto_filtrado.append(quartos[j])
            except IndexError:
                continue

        driver.find_element_by_xpath("//a[@title='Próxima página']").click() 

    time.sleep(2)
    driver.quit()

    create_dataframe(bairro_filtrado, quarto_filtrado, preco_filtrado)

if __name__ == '__main__':
    main()