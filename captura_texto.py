import requests
from bs4 import BeautifulSoup
import pandas as pd


def extraiTexto(link):
    response = requests.get(link)
    content = response.content
    site = BeautifulSoup(content, 'html.parser')
    link_real = site.find('script')
    link_real = str(link_real).split('"')
    link_real = link_real[1]

    response = requests.get(link_real)
    content = response.content
    site = BeautifulSoup(content, 'html.parser')
    try:
        noticia = site.find('div', attrs={'class': 'materia-conteudo entry-content clearfix'})
        return noticia.text
    except:
        pass
    try:
        noticia = site.find('div', attrs={'class': 'entry'})
        return noticia.text
    except:
        pass
    try:
        noticia = site.find('article')
        return noticia.text
    except:
        pass
    print('Erro')
    return ''

tags = ['economia', 'avião', 'aéreo', 'viagem', 'viajar', 'turismo', 'linhas aéreas', 'aeroporto']

for tag in tags:
    for ano in range(2010, 2013):
        df = pd.read_excel('SaidaSeparadaAno/' + tag + '_' + str(ano) + '.xlsx')
        df['texto'] = df['LinkLimpo'].apply(lambda x: extraiTexto(x))
        df.to_excel('saidaTexto/' + tag + str(ano) + '.xlsx', index=False, engine='xlsxwriter')