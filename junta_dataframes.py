import pandas as pd


def Join(tags):
    df_final = pd.DataFrame()
    for tag in tags:
        df = pd.read_excel('saidaFinal/' + tag + '.xlsx')
        print(df)
        df_final = pd.concat([df_final, df])
    df_final = df_final.drop_duplicates()
    return df_final


tags = ['economia', 'avião', 'aéreo', 'viagem', 'viajar', 'turismo', 'linhas aereas', 'aeroporto']


for tag in tags:
    df_final = pd.DataFrame()
    for ano in range(2007, 2019):
        df = pd.read_excel('saidaTexto/' + tag + str(ano) + '.xlsx')
        df.drop(['Data', 'LinkLimpo'], inplace=True, axis=1)
        df_final = pd.concat([df_final, df])
    df_final.to_excel('saidaFinal/' + tag + '.xlsx', index=False, engine='xlsxwriter')



tags_turismo = ['viagem', 'viajar', 'turismo']
tags_aereo = ['avião', 'aéreo', 'linhas aereas', 'aeroporto']
tags_economia = ['economia']

df_macro = Join(tags_macro)
df_macro.to_csv('Titulo/saidaJoin/turismo.csv', index=False)
df_micro = Join(tags_micro)
df_micro.to_csv('Titulo/saidaJoin/aereo.csv', index=False)
df_economia = Join(tags_economia)
df_economia.to_csv('Titulo/saidaJoin/economia.csv', index=False)