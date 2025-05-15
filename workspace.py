#importanto bibliotecas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import locale

#funções---------------------------------------------------------------------------------
def remover_outliers(df, coluna_valor):
    Q1 = df[coluna_valor].quantile(0.25)
    Q3 = df[coluna_valor].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    return df[(df[coluna_valor] >= limite_inferior) & (df[coluna_valor] <= limite_superior)]
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


#gerando as datas dos arquivos xlsx

df_IPCA_cafemoido = df_IPCA_cafemoido.transpose()
df_IPCA_cafemoido = df_IPCA_cafemoido.reset_index()
df_IPCA_cafemoido = df_IPCA_cafemoido.drop(index=0)
df_IPCA_cafemoido.columns = ['data', 'Brasil', 'Belém', 'Fortaleza', 'Recife','Salvador','Belo Horizonte', 'Grande Vitória', 'Rio de Janeiro', 'São Paulo', 'Curitiba', 'Porto Alegre']
locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
df_IPCA_cafemoido['data'] = pd.to_datetime(df_IPCA_cafemoido['data'], format='%B %Y')

df_IPCA_geral = df_IPCA_geral.T.reset_index()
df_IPCA_geral = df_IPCA_geral.drop(index=0)
df_IPCA_geral.columns = ['data', 'Brasil', 'Belém', 'Fortaleza', 'Recife','Salvador','Belo Horizonte', 'Grande Vitória', 'Rio de Janeiro', 'São Paulo', 'Curitiba', 'Porto Alegre']
df_IPCA_geral['data'] = pd.to_datetime(df_IPCA_geral['data'], format='%B %Y')

df_IPCA_alimentacao = df_IPCA_alimentacao.T.reset_index()
df_IPCA_alimentacao = df_IPCA_alimentacao.drop(index=0)
df_IPCA_alimentacao.columns = ['data', 'Brasil', 'Belém', 'Fortaleza', 'Recife','Salvador','Belo Horizonte', 'Grande Vitória', 'Rio de Janeiro', 'São Paulo', 'Curitiba', 'Porto Alegre']
df_IPCA_alimentacao['data'] = pd.to_datetime(df_IPCA_alimentacao['data'], format='%B %Y')

#Buscando dados faltantes---------------------------------------------------------------
"""
print(df_robusta.isnull().sum()) #0 missing data
print(df_arabica.isnull().sum()) #0 missing data
print(df_salariomin.isnull().sum()) #0 missing data
print(df_IPCA_cafemoido.isnull().sum()) #0 missing data
print(df_IPCA_geral.isnull().sum()) #0 missing data
print(df_IPCA_alimentacao.isnull().sum()) #0 missing data
"""
#Separando os dados em diferentes escalas temporais e removendo outliers--------------------------------------

df_robusta['ano_mes'] = df_robusta['data'].dt.to_period('M')
df_robusta_N_outlier = remover_outliers(df_robusta, 'preco_reais')
df_robusta_N_outlier['ano_mes'] = df_robusta_N_outlier['data'].dt.to_period('M')
df_robusta_M = df_robusta_N_outlier.groupby('ano_mes')['preco_reais'].mean().reset_index()
df_robusta_N_outlier['ano'] = pd.to_datetime(df_robusta_N_outlier['data']).dt.year
df_robusta_Y = df_robusta_N_outlier.groupby('ano')["preco_reais"].mean().reset_index()


df_arabica['ano_mes'] = df_arabica['data'].dt.to_period('M')
df_arabica_N_outlier = remover_outliers(df_arabica, 'preco_reais')
df_arabica_N_outlier['ano_mes'] = df_arabica_N_outlier['data'].dt.to_period('M')
df_arabica_M = df_arabica_N_outlier.groupby('ano_mes')['preco_reais'].mean().reset_index()
df_arabica_N_outlier['ano'] = pd.to_datetime(df_arabica_N_outlier['data']).dt.year
df_arabica_Y = df_arabica_N_outlier.groupby('ano')["preco_reais"].mean().reset_index()

#Para IPCA o valor anual deve ser tirado a partir da variação acumulada

df_IPCA_cafemoido['ano'] = pd.to_datetime(df_IPCA_cafemoido['data']).dt.year
df_IPCA_cafemoido['fator'] = 1 + (df_IPCA_cafemoido['São Paulo']/100)
df_IPCA_cafemoidoSP_Y = df_IPCA_cafemoido.groupby('ano')['fator'].prod().reset_index()
df_IPCA_cafemoidoSP_Y['IPCA_acumulado_%'] = (df_IPCA_cafemoidoSP_Y['fator'] - 1) * 100

df_IPCA_alimentacao['ano'] = pd.to_datetime(df_IPCA_alimentacao['data']).dt.year
df_IPCA_alimentacao['fator'] = 1 + (df_IPCA_alimentacao['São Paulo']/100)
df_IPCA_alimentacaoSP_Y = df_IPCA_alimentacao.groupby('ano')['fator'].prod().reset_index()
df_IPCA_alimentacaoSP_Y['IPCA_acumulado_%'] = (df_IPCA_alimentacaoSP_Y['fator'] - 1) * 100

df_IPCA_geral['ano'] = pd.to_datetime(df_IPCA_geral['data']).dt.year
df_IPCA_geral['fator'] = 1 + (df_IPCA_geral['São Paulo']/100)
df_IPCA_geralSP_Y = df_IPCA_geral.groupby('ano')['fator'].prod().reset_index()
df_IPCA_geralSP_Y['IPCA_acumulado_%'] = (df_IPCA_geralSP_Y['fator'] - 1) * 100

print(df_IPCA_cafemoidoSP_Y)
#Gerando gráficos------------------------------------------------------------------------

palette = ["#2980B9"] * 6

'''
#OUTLIERS ROBUSTA

plt.figure(figsize=(10, 6))
sns.set_style("darkgrid")
sns.boxplot(data=df_robusta, x='ano', y='preco_reais', palette=palette)

plt.title('Evolução Anual dos Preços Diários do Café Robusta (2020–2025)',
          fontsize=14, weight='bold', color="#2C3E50")
plt.xlabel('Ano', fontsize=12, color="#2C3E50")
plt.ylabel('Preço do Café (R$ por 60kg)', fontsize=12, color="#2C3E50")
plt.xticks(fontsize=11, color="#2C3E50")
plt.yticks(fontsize=11, color="#2C3E50")
sns.despine()
plt.gca().set_facecolor("#FDF6E3")  
plt.tight_layout()
plt.show()
'''
#Para economizar tempo e linhas não vou deixar os próximos cod boxplot documentados

'''plt.figure(figsize=(10,6))
sns.set_style('darkgrid')
sns.boxplot(data=df_IPCA_geral, x='ano', y='São Paulo')
plt.title('IPCA Geral em São Paulo (2020–2025)',
          fontsize=14, weight='bold', color="#2C3E50")
plt.xlabel('Ano', fontsize=12, color="#2C3E50")
plt.ylabel('IPCA Geral', fontsize=12, color="#2C3E50")
plt.xticks(fontsize=11, color="#2C3E50")
plt.yticks(fontsize=11, color="#2C3E50")
sns.despine()
plt.gca().set_facecolor("#FDF6E3") 
plt.tight_layout()
plt.show()'''