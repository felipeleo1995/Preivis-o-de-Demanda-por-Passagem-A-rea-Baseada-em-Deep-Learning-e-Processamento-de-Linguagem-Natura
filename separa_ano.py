
import pandas as pd

def getAno(data):
    return data.year


tags = ['economia', 'avião', 'aéreo', 'viagem', 'viajar', 'turismo', 'linhas aéreas', 'aeroporto']

for tag in tags:
    df = pd.read_excel('limpos/Links_limpos_' + tag + '.xlsx')
    df['Data'] = pd.to_datetime(df['Data'].astype(str), format='%Y-%m-%d')
    df['Ano'] = df.apply(lambda row: getAno(row['Data']), axis = 1)
    for ano in range(2006, 2019):
        df_novo = df[df['Ano'] == ano]
        df_novo.to_excel('SaidaSeparadaAno/' + tag + '_' + str(ano) + '.xlsx', index=False, engine='xlsxwriter')
        print(df_novo)