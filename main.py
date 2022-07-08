import pandas as pd
import re
import nltk
from unicodedata import normalize
import csv

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

STEMMER = SnowballStemmer('portuguese')
STOPWORDS = stopwords.words('portuguese')
REGEXP_REMOVE_SPECIAL = re.compile('[^a-zA-Z0-9 ]+')
TRAIN_PERCENTAGE_SIZE = 60 / 100
TEST_PERCENTAGE_SIZE = 20 / 100


# Limpa o texto, passa tudo para minúscula, remove as stopwords, Stemiza todas as palavras e passa tudo para o padrão ASCII
def getCleanText(text):
    finalTextArray = []
    lowerText = text.lower()
    teste = 0
    for word in lowerText.split():
        teste = teste + 1
        if word not in STOPWORDS:
            finalTextArray.append(STEMMER.stem(word))
    finalText = ' '.join(finalTextArray)
    finalText = normalize('NFKD', finalText).encode('ASCII', 'ignore').decode('ASCII')
    finalText = REGEXP_REMOVE_SPECIAL.sub('', finalText)
    finalText = re.sub(' +', ' ', finalText)
    return finalText

bases = ['economia', 'aereo', 'turismo']

for tag in bases:
    # Lê a base de dados bruta
    articles = pd.read_excel('saidaJoin/' + tag + '.xlsx')
    demand = pd.read_excel('demanda.xlsx')

    # Retira da base as notícias sem texto
    articles = articles[articles.texto.isnull() == False]

    # Limpa todos os textos das notícias usando a função getCleanText
    articles['texto'] = articles['texto'].apply(lambda x: getCleanText(x))

    # Junta o dataframe de notícias com o dataframe de variação na demanda por transporte aéreo usando a coluna 'date' como referência
    articles = articles.merge(demand, how='inner', on='Ano')
    articles.drop('Ano', inplace=True, axis=1)
    articles.columns = ['text', 'label']

    # Organiza a lista de notícias de forma randômica
    articles = articles.sample(frac=1)
    articles['label'] = pd.to_numeric(articles['label'])
    cols = articles.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    articles = articles[cols]

    # Contabiliza o número de notícias para a base de treino, teste e validação
    trainSize = round(len(articles) * (TRAIN_PERCENTAGE_SIZE))
    testSize = round(len(articles) * (TEST_PERCENTAGE_SIZE))

    # Separa as bases em arquivos diferentes
    data_train = articles.head(trainSize)
    data_test = articles.iloc[trainSize:(trainSize + testSize)]
    data_validation = articles.iloc[(trainSize + testSize):]

    data_train.to_csv('saidaBaseFinal/data_train_' + tag + '.csv', index=False, header=False)
    data_train.to_csv('saidaBaseFinal/data_train_' + tag + '_TSV.tsv', sep='\t', quoting=csv.QUOTE_NONE, index=False, header=False)
    data_test.to_csv('saidaBaseFinal/data_test_' + tag + '.csv', index=False, header=False)
    data_test.to_csv('saidaBaseFinal/data_test_' + tag + '_TSV.tsv', sep='\t', quoting=csv.QUOTE_NONE, index=False, header=False)
    data_validation.to_csv('saidaBaseFinal/data_validation_' + tag + '.csv', index=False, header=False)
    data_validation.to_csv('saidaBaseFinal/data_validation_' + tag + '_TSV.tsv', sep='\t', quoting=csv.QUOTE_NONE, index=False, header=False)
