import pandas as pd


def getCleanLink(link):
    # Retira da base as notícias sem texto (apenas vídeo)
    if 'video' in link or 'globoplay' in link:
        linklimpo = None
    else:
        linklimpo = link
        print('Deu bom para o link:')
        print(link)
    return linklimpo

lista_de_palavras = ['economia', 'avião', 'aéreo', 'viagem', 'viajar', 'turismo', 'linhas aéreas', 'aeroporto']

for palavra in lista_de_palavras:
    links_final = pd.DataFrame()
    for mes in range(259, 18, -1):
        try:
            links = pd.read_csv('saida/noticias_' + palavra + '_' + str(mes) + '.csv')
            links['LinkLimpo'] = links['Link'].apply(lambda x: getCleanLink(x))
            links = links[links.LinkLimpo.isnull() == False]
            links_final = links_final.append(links)
        except:
            print('Erro ao identificar o arquivo')
    try:
        links_final = links_final.sort_values('Data')
        links_final.drop(columns=['Link'], inplace=True)
        links_final.to_excel('limpos/Links_limpos_' + palavra + '.xlsx', index=False)
    except:
        print('Erro ao criar o arquivo')
