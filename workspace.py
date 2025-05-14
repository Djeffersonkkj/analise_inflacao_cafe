#Extraindo das tabelas apenas os dados que são do meu interesse

#importanto bibliotecas
import pandas as pd
import locale

#trazendo os dados-----------------------------------------------------------------------

df_robusta = pd.read_csv('dados\cafe_robusta_CEPEA_20250508215926.csv', encoding='latin1', sep=';', decimal=',', skiprows=3)
df_robusta = df_robusta.dropna(axis=1, how='all')
df_robusta.columns = ['data', 'preco_reais', 'preco_dolar']
df_robusta = df_robusta.drop(columns=['preco_dolar'])

df_arabica = pd.read_csv('dados\cafe_arabica_CEPEA_20250508220547.csv', encoding='latin1', sep=';', decimal=',', skiprows=3)
df_arabica = df_arabica.dropna(axis=1, how='all')
df_arabica.columns = ['data', 'preco_reais', 'preco_dolar']
df_arabica = df_arabica.drop(columns=['preco_dolar'])

df_salariomin = pd.read_csv('dados\salariominimo.csv', encoding='latin1', sep=';', decimal=',')
df_salariomin.columns = ['A partir de', 'Valor em reais', 'Legislação', 'Total reajustado']
df_salariomin = df_salariomin.drop(columns=['Legislação'])

df_IPCA_cafemoido = pd.read_excel('dados\IPCAcafemoido.xlsx', skiprows=3)

df_IPCA_geral = pd.read_excel('dados\IPCAgeral.xlsx', skiprows=3)

df_IPCA_alimentacao = pd.read_excel('dados\IPCAalimentacao.xlsx', skiprows=3)

#Limitando período jan 2020 - abril 2025 -------------------------------------------------

df_robusta['data'] = pd.to_datetime(df_robusta['data'], dayfirst=True)
df_robusta = df_robusta[(df_robusta['data'] >= '2020-01-01') & (df_robusta['data'] <= '2025-04-30')]

df_arabica['data'] = pd.to_datetime(df_arabica['data'], dayfirst=True)
df_arabica = df_arabica[(df_arabica['data'] >= '2020-01-01') & (df_arabica['data'] <= '2025-04-30')]

df_salariomin = df_salariomin[28:]

'''
Os dados da planilha não precisão de filtro pois já estão no período desejado. Mas vou deixar o código aqui por fins de aprendizado

df_IPCA_cafemoido = df_IPCA_cafemoido.transpose()
df_IPCA_cafemoido = df_IPCA_cafemoido.reset_index()
df_IPCA_cafemoido = df_IPCA_cafemoido.drop(index=0)
df_IPCA_cafemoido.columns = ['data', 'Brasil', 'Belém', 'Fortaleza', 'Recife','Salvador','Belo Horizonte', 'Grande Vitória', 'Rio de Janeiro', 'São Paulo', 'Curitiba', 'Porto Alegre']
locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
df_IPCA_cafemoido['data'] = pd.to_datetime(df_IPCA_cafemoido['data'], format='%B %Y')
df_IPCA_cafemoido = df_IPCA_cafemoido[(df_IPCA_cafemoido['data'] >= '2020-01-01') & (df_IPCA_cafemoido['data'] <= '2025-04-30')]
'''


print(df_IPCA_cafemoido)
