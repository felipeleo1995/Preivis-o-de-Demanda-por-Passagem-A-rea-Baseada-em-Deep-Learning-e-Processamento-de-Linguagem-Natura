from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
from datetime import datetime
from datetime import date
from selenium.webdriver.common.keys import Keys


# Rola a página para baixo 4 vezes para mostrar mais notícias
def rolar_pag_baixo():
    for c in range(0, 4):
        sleep(timer)
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# Clica em "Aplicar"
def clicar_aplicar():
    botao_aplicar = navegador.find_element_by_css_selector(
        'div > div > div > div > div > div > div > div > div > button')
    botao_aplicar.click()
    sleep(timer)


# Clica no botão de "Ver Mais" até o limite para mostrar todas as notícias
def clilcar_vermais():
    pagina = BeautifulSoup(navegador.page_source, 'html.parser')
    cards = pagina.findAll('div', attrs={'class': 'widget--info__text-container'})  # Pega todos os cards da página atual
    while (len(cards) < 600):  # 600 é o limite de notícias por página
        try:
            botao_ver_mais = navegador.find_element_by_css_selector('section > div > div > div > a')
        except:
            break
        botao_ver_mais.click()
        sleep(timer)
        pagina = BeautifulSoup(navegador.page_source, 'html.parser')
        cards = pagina.findAll('div', attrs={'class': 'widget--info__text-container'})


# Extrai as informações das notícias da tela e armazena em csv
def extrai_infos():
    pagina = BeautifulSoup(navegador.page_source, 'html.parser')
    cards = pagina.findAll('div',
                           attrs={'class': 'widget--info__text-container'})  # Pega todos os cards da página atual
    for card in cards:
        try:
            titulo = card.find('div', attrs={'class': 'widget--info__title product-color'}).text
        except:
            titulo = ''
        data = card.find('div', attrs={'class': 'widget--info__meta'})
        if data.text.split()[0] == 'há':
            data = date.today()
        else:
            data = datetime.strptime(data.text.split()[0], '%d/%m/%Y').date()
        link = 'https:' + card.find('a')['href']
        lista_noticias.append([data, titulo, link])


# Seleciona o primeiro dia do mês
def clicar_dia1():
    calendario = navegador.find_elements_by_tag_name('tbody')[1]  # Identifica o calendário
    primeira_semana = calendario.find_elements_by_tag_name('tr')[0]  # Identifica a primeira semana
    dias = primeira_semana.find_elements_by_tag_name(
        'td')  # Identifica a lista com todos os dias da primeira semana do mês
    for dia in dias:  # Identifica o primeiro dia do mês
        if (dia.text == '1'):
            sleep(1)
            dia.click()
    sleep(timer)


# Seleciona o dia 8
def clicar_dia8():
    calendario = navegador.find_elements_by_tag_name('tbody')[1]
    segunda_semana = calendario.find_elements_by_tag_name('tr')[1]
    dias = segunda_semana.find_elements_by_tag_name('td')
    for dia in dias:
        if (dia.text == '8'):
            sleep(1)
            dia.click()
    sleep(timer)


# Seleciona o dia 15
def clicar_dia15():
    calendario = navegador.find_elements_by_tag_name('tbody')[1]
    terceira_semana = calendario.find_elements_by_tag_name('tr')[2]
    dias = terceira_semana.find_elements_by_tag_name('td')
    for dia in dias:
        if (dia.text == '15'):
            sleep(1)
            dia.click()
    sleep(timer)


# Seleciona o dia 15
def clicar_dia22():
    calendario = navegador.find_elements_by_tag_name('tbody')[1]
    quarta_semana = calendario.find_elements_by_tag_name('tr')[3]
    dias = quarta_semana.find_elements_by_tag_name('td')
    for dia in dias:
        if (dia.text == '22'):
            sleep(1)
            dia.click()
    sleep(timer)


# Seleciona o último dia do mês
def clicar_ultimo_dia():
    calendario = navegador.find_elements_by_tag_name('tbody')[1]
    ultima_semana = calendario.find_elements_by_tag_name('tr')[-1]
    dias = ultima_semana.find_elements_by_tag_name('td')
    for dia in dias:
        if (dia.text != ''):
            ultimo_dia = dia
    ultimo_dia.click()
    sleep(timer)


# Pesquisa as palavras chave no campo de busca de notícias
def pesquisa(palavra):
    navegador.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
    try:
        campo = navegador.find_element_by_tag_name('fieldset')
        input_place = campo.find_element_by_tag_name('input')
    except:
        input_place = navegador.find_element_by_tag_name('input')
        caracteres_pesquisa = len(input_place.get_attribute('value'))
        input_place.send_keys(caracteres_pesquisa * Keys.BACKSPACE)
    input_place.send_keys(palavra)
    input_place.submit()
    sleep(timer)

# Tags que serão pesquisadas
lista_de_palavras = ['economia', 'avião', 'aéreo', 'viagem', 'viajar', 'turismo', 'linhas aéreas', 'aeroporto']


# Intervalo de tempo para garantir que os elementos foram carregados na página antes de tentar acessar
timer = 2

# Inibe o Selenium de abrir o navegador real para mostrar o que tá acontecendo
options = Options()
options.add_argument('--headless')
options.add_argument(('window-size=1920,1080'))

# Navegador do Selenium pra acessar a página inicial
navegador = webdriver.Chrome(options=options)
navegador.get('https://g1.globo.com/')

# Clica no botão do banner de cockies (necessário para poder prosseguir)
botao_cokies = navegador.find_element_by_id('cookie-banner-lgpd')
botao_cokies = botao_cokies.find_element_by_class_name('cookie-banner-lgpd_accept-button')
botao_cokies.click()


for palavra in lista_de_palavras:
    for mes in range(259, 18, -1):
        # Lista onde serão armazenadas as notícias e seus links
        lista_noticias = []

        # Pesquisa as palavras chave no  campo de busca de notícias e filtra pelas mais relevantes
        pesquisa(palavra)
        barra_filtro = navegador.find_element_by_id('search-filter-component')
        barra_filtro = barra_filtro.find_element_by_css_selector('div > div > div> div')
        botao_ordenar = barra_filtro.find_element_by_class_name('filters__container')
        botao_ordenar = botao_ordenar.find_elements_by_css_selector('div > a')[1]
        botao_ordenar.click()
        sleep(timer)
        botao_relevancia = barra_filtro.find_element_by_class_name('filters__container')
        botao_relevancia = botao_relevancia.find_elements_by_css_selector('div > ul > li')[8]
        botao_relevancia.click()
        sleep(timer)

        # Clica no botão de "filtrar por data"
        barra_filtro = barra_filtro.find_element_by_class_name('filters__advanced-date-filter')
        botao_filtro = barra_filtro.find_element_by_class_name('filters__dropdown__link')
        botao_filtro.click()
        sleep(timer)

        # Clica em "período personalizado"
        botao_periodo = barra_filtro.find_element_by_class_name('filters__dropdown__list__right')
        botao_periodo = botao_periodo.find_element_by_class_name('filters__dropdown__list__range-date')
        botao_periodo.click()
        sleep(timer)

        # Identifica o botão de voltar 1 mês
        botao_voltar = navegador.find_element_by_id('search-filter-component')
        botao_voltar = botao_voltar.find_element_by_class_name('range-date-filter-modal__container')
        botao_voltar = botao_voltar.find_element_by_class_name('range-date-filters')
        botao_voltar = botao_voltar.find_element_by_css_selector('div > div > div > div > div > div > svg')

        # Clica no botão "voltar" a quantidade de vezes necessária para chegar na data correta
        contador = 0
        while (contador < mes):
            contador = contador + 1
            botao_voltar.click()
            sleep(.3)

        # Extrai os dados da primeira semana
        clicar_dia1()  # Seleciona o primeiro dia do mês
        clicar_dia8()  # Seleciona o dia 8
        clicar_aplicar()  # Clica em "Aplicar"
        rolar_pag_baixo()  # Rola a página para baixo para mostrar mais notícias
        clilcar_vermais()  # Clica no botão de "Ver Mais" até o limite para mostrar todas as notícias
        extrai_infos()  # Extrai as informações das notícias da tela e armazena em csv

        # Extrai os dados da segunda semana
        botao_filtro.click()
        sleep(timer)
        botao_periodo.click()
        sleep(timer)
        clicar_dia8()
        clicar_dia15()
        clicar_aplicar()
        rolar_pag_baixo()
        clilcar_vermais()
        extrai_infos()

        # Extrai os dados da terceira semana
        botao_filtro.click()
        sleep(timer)
        botao_periodo.click()
        sleep(timer)
        clicar_dia15()
        clicar_dia22()
        clicar_aplicar()
        rolar_pag_baixo()
        clilcar_vermais()
        extrai_infos()

        # Extrai os dados do resto do mês
        botao_filtro.click()
        sleep(timer)
        botao_periodo.click()
        sleep(timer)
        clicar_dia22()
        clicar_ultimo_dia()
        clicar_aplicar()
        rolar_pag_baixo()
        clilcar_vermais()
        extrai_infos()

        # Armazena as informações em csv
        noticias_df = pd.DataFrame(lista_noticias, columns=['Data', 'Titulo', 'Link'])
        noticias_df.to_csv('saida/noticias_' + palavra + '_' + str(mes) + '.csv', index=False)


