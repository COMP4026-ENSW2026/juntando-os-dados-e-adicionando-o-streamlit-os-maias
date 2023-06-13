import urllib.request
from bs4 import BeautifulSoup
from classImovel import Imovel
import pandas as pd

pages = [1,2,3]
url = "https://www.catuaiimoveis.com.br"
tabulka_lis = []

for page in pages:
  # https://www.catuaiimoveis.com.br/imoveis/apartamento-a-venda-londrina/#imoveis
  fp = urllib.request.urlopen(url + "/imoveis/apartamento-a-venda-londrina//" + str(page))

  mybytes = fp.read()

  fp.close()

  soup = BeautifulSoup(mybytes)
  mystr = mybytes.decode("utf8")

  # Captura itens da home
  # tabulka = soup.find_all("div", {"class" : "dados-if"})

  # captura container de iten da pagina de lista
  tabulka_ul = soup.find("ul", {"class" : "lista-imovel-filtro"})
  tabulka_lis = [*tabulka_lis , *tabulka_ul.children]

# captura os itens dentro do container da pagina de lista

# mostra todo o html no console
# print(tabulka_lis)

lista_de_imoveis = []

for value in tabulka_lis:
  try:
    imovel_link_detalhes = value.find("a", {"class": "imovel-mobile"})['href']
    tabulka_value = value.find("div", {"class": "demais-infos"})

    tipo_imovel = tabulka_value.find("h4").get_text()
    nome_imovel = tabulka_value.find("h1").get_text()
    valor_imovel = tabulka_value.find("span", {"class":"valores"}).find("strong").get_text()
    cidade_imovel = tabulka_value.find("span", {"class":"cidade-detalhes"}).get_text()
    detalhes_imovel = tabulka_value.find("div", {"class":"detalhes"})

    dormitorios = detalhes_imovel.span.get_text()
    detalhes_imovel.span.decompose()

    banheiros = detalhes_imovel.span.get_text()
    detalhes_imovel.span.decompose()

    vagas = detalhes_imovel.span.get_text()
    detalhes_imovel.span.decompose()
    
    imovel_pesquisado = Imovel(tipo_imovel,nome_imovel,valor_imovel,cidade_imovel, dormitorios, banheiros, vagas)
    lista_de_imoveis.append(imovel_pesquisado)
  except Exception as e: print(e)


lst = [[x.tipo_imovel,x.nome_imovel,x.valor_imovel,x.cidade_imovel, x.dormitorios, x.banheiros, x.vagas] for x in lista_de_imoveis]

df = pd.DataFrame(lst, columns=["tipo_imovel", "nome_imovel", "valor_imovel", "cidade_imovel", "dormitorios","banheiros", "vagas"])
df.to_csv('my_file.csv', index=False, header=False)


