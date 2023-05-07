import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

url_input = st.text_input("Insira a URL do site para fazer o scrape:", "https://www.raulfulgencio.com.br/comprar/Londrina/Apartamento")

fp = urllib.request.urlopen(url_input)
mybytes = fp.read()
fp.close()

soup = BeautifulSoup(mybytes, 'html.parser')
property_listing = soup.find("div", {"id" : "property-listing"})
row = property_listing.find("div", {"class" : "row"})

bar = st.progress(0)

lista_de_imoveis = []

for i, item in enumerate(row.children):
    try:
        price = item.find("div", {"class":"price"}).span.get_text()
        valor_imovel = price

        infos = item.find("div", { "class": "info"})

        first_session = infos.find("div", {"class" : "amenities"})
        tipo_imovel = first_session.a.get_text()
        first_session.decompose()

        second_session = infos.find("div", {"class" : "amenities"})
        detalhes_imovel = infos.find("ul",{"class":"imo-itens"})

        dormitorios = detalhes_imovel.li.get('title')
        detalhes_imovel.li.decompose()
        banheiros = detalhes_imovel.li.get('title')
        detalhes_imovel.li.decompose()
        vagas = detalhes_imovel.li.get('title')
        detalhes_imovel.li.decompose()
        second_session.decompose()

        third_session = infos.find("div", {"class" : "amenities"})
        third_session.p.strong.decompose()    
        nome_imovel = third_session.p.get_text().split('-')[1]

        cidade_imovel = "Londrina"

        imovel_pesquisado = Imovel(tipo_imovel,nome_imovel,valor_imovel,cidade_imovel, dormitorios, banheiros, vagas)
        lista_de_imoveis.append(imovel_pesquisado)
    except Exception as e:
        print(e)

    # Atualizar o progress bar
    bar.progress((i + 1) / len(row.children))

df = pd.DataFrame(lista_de_imoveis, columns=["tipo_imovel", "nome_imovel", "valor_imovel", "cidade_imovel", "dormitorios","banheiros", "vagas"])

st.write(df)
