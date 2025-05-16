#importanto bibliotecas-----------------------------------------------------------------
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import locale
locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')

#funções---------------------------------------------------------------------------------
def processar_IPCA(df):
    df = df.T.reset_index()
    df = df.drop(index=0)
    df.columns = ['data', 'Brasil', 'Belém', 'Fortaleza', 'Recife', 'Salvador', 'Belo Horizonte', 'Grande Vitória', 'Rio de Janeiro', 'São Paulo', 'Curitiba', 'Porto Alegre']
    df['data'] = pd.to_datetime(df['data'], format='%B %Y')
    return df

#trazendo os dados-----------------------------------------------------------------------
df_robusta = pd.read_csv('dados/cafe_robusta_CEPEA_20250508215926.csv', encoding='latin1', sep=';', decimal=',', skiprows=3)
df_robusta = df_robusta.dropna(axis=1, how='all')
df_robusta.columns = ['data', 'preco_reais', 'preco_dolar']
df_robusta = df_robusta.drop(columns=['preco_dolar'])

df_arabica = pd.read_csv('dados/cafe_arabica_CEPEA_20250508220547.csv', encoding='latin1', sep=';', decimal=',', skiprows=3)
df_arabica = df_arabica.dropna(axis=1, how='all')
df_arabica.columns = ['data', 'preco_reais', 'preco_dolar']
df_arabica = df_arabica.drop(columns=['preco_dolar'])

df_salariomin = pd.read_csv('dados/salariominimo.csv', encoding='latin1', sep=';', decimal=',')
df_salariomin.columns = ['ano_mes', 'salario_min', 'legislação', 'total_reajustado']
df_salariomin = df_salariomin.drop(columns=['legislação'])
df_salariomin['salario_min'] = df_salariomin['salario_min'].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').astype(float)

df_IPCA_cafemoido = pd.read_excel('dados/IPCAcafemoido.xlsx', skiprows=3)

df_IPCA_geral = pd.read_excel('dados/IPCAgeral.xlsx', skiprows=3)

df_IPCA_alimentacao = pd.read_excel('dados/IPCAalimentacao.xlsx', skiprows=3)

#Limitando período jan 2020 - abril 2025 -------------------------------------------------
df_robusta['data'] = pd.to_datetime(df_robusta['data'], dayfirst=True)
df_robusta = df_robusta[(df_robusta['data'] >= '2020-01-01') & (df_robusta['data'] <= '2025-04-30')]

df_arabica['data'] = pd.to_datetime(df_arabica['data'], dayfirst=True)
df_arabica = df_arabica[(df_arabica['data'] >= '2020-01-01') & (df_arabica['data'] <= '2025-04-30')]

df_salariomin = df_salariomin[28:]
df_salariomin['ano_mes'] = pd.to_datetime(df_salariomin['ano_mes'], format='%B de %Y')

#gerando as datas dos arquivos xlsx
df_IPCA_cafemoido = processar_IPCA(df_IPCA_cafemoido)
df_IPCA_geral = processar_IPCA(df_IPCA_geral)
df_IPCA_alimentacao = processar_IPCA(df_IPCA_alimentacao)


#Buscando dados faltantes---------------------------------------------------------------
"""
print(df_robusta.isnull().sum()) #0 missing data
print(df_arabica.isnull().sum()) #0 missing data
print(df_salariomin.isnull().sum()) #0 missing data
print(df_IPCA_cafemoido.isnull().sum()) #0 missing data
print(df_IPCA_geral.isnull().sum()) #0 missing data
print(df_IPCA_alimentacao.isnull().sum()) #0 missing data
"""
#Criando diferentes escalas temporais-------------------------------------

df_robusta['ano_mes'] = df_robusta['data'].dt.to_period('M')
df_robusta_M = df_robusta.groupby('ano_mes')['preco_reais'].mean().reset_index()
df_robusta_M['ano_mes'] = df_robusta_M['ano_mes'].dt.to_timestamp()
df_robusta['ano'] = df_robusta['data'].dt.year
df_robusta_Y = df_robusta.groupby('ano')["preco_reais"].mean().reset_index()


df_arabica['ano_mes'] = df_arabica['data'].dt.to_period('M')
df_arabica_M = df_arabica.groupby('ano_mes')['preco_reais'].mean().reset_index()
df_arabica_M['ano_mes'] = df_arabica_M['ano_mes'].dt.to_timestamp()
df_arabica['ano'] = df_arabica['data'].dt.year
df_arabica_Y = df_arabica.groupby('ano')["preco_reais"].mean().reset_index()
#Para IPCA o valor anual deve ser tirado a partir da variação acumulada

df_IPCA_cafemoido['ano'] = pd.to_datetime(df_IPCA_cafemoido['data']).dt.year
df_IPCA_cafemoido['fator'] = 1 + (df_IPCA_cafemoido['São Paulo']/100)
df_IPCA_cafemoido['mes'] = pd.to_datetime(df_IPCA_cafemoido['data']).dt.month
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

#Filtros---------------------------------------------------------------------------------

df_IPCA_cafemoido_quadrimestre = df_IPCA_cafemoido[df_IPCA_cafemoido['mes'] <= 4].copy()
df_IPCA_cafemoido_quadrimestre['fator'] = 1 + (df_IPCA_cafemoido_quadrimestre['São Paulo'] / 100)
df_IPCA_cafe_acumulado = (
    df_IPCA_cafemoido_quadrimestre.groupby('ano')['fator']
    .prod()
    .sub(1)         # subtrai 1 para voltar ao valor percentual
    .mul(100)       # converte para porcentagem
    .reset_index(name='IPCA_acumulado')
)
#Tratando dados para gráficos------------------------------------------------------------

df_arabica_M['valor_kg'] = df_arabica_M['preco_reais'] / 60
df_robusta_M['valor_kg'] = df_robusta_M['preco_reais'] / 60
df_temp = pd.merge(df_robusta_M, df_arabica_M, on='ano_mes', how='inner', suffixes=('_robusta', '_arabica'))
df_sal_cafe = pd.merge(df_temp, df_salariomin[['ano_mes', 'salario_min']], on='ano_mes', how='left')
df_sal_cafe['salario_min'] = df_sal_cafe['salario_min'].ffill()
df_sal_cafe['kg_cafe_robusta_compra'] = df_sal_cafe['salario_min'] / df_sal_cafe['valor_kg_robusta']
df_sal_cafe['kg_cafe_arabica_compra'] = df_sal_cafe['salario_min'] / df_sal_cafe['valor_kg_arabica']

df_salariomin_limpo = pd.DataFrame({
    'ano': [2020, 2021, 2022, 2023, 2024, 2025],
    'reajuste_%': [4.68, 5.26, 10.16, 8.90, 6.97, 7.95]
})
df_IPCA = pd.DataFrame({'ano': df_IPCA_cafemoidoSP_Y['ano']})
df_IPCA = df_IPCA.merge(df_IPCA_cafemoidoSP_Y[['ano', 'IPCA_acumulado_%']], on='ano', how='left')
df_IPCA = df_IPCA.merge(df_IPCA_geralSP_Y[['ano', 'IPCA_acumulado_%']], on='ano', how='left', suffixes=('_cafe', '_geral'))
df_IPCA = df_IPCA.merge(df_IPCA_alimentacaoSP_Y[['ano', 'IPCA_acumulado_%']], on='ano', how='left')
df_IPCA = df_IPCA.merge(df_salariomin_limpo, on='ano', how='left')
df_IPCA.columns = ['ano', 'IPCA_cafe', 'IPCA_geral', 'IPCA_alimentacao', 'reajuste_salariomin']

#Gerando gráficos------------------------------------------------------------------------


def grafico1():
    #OUTLIERS ROBUSTA
    palette = ["#2980B9"] * 6
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
    
    #Para economizar tempo e linhas não vou deixar os próximos cod boxplot documentados

def grafico2():
    #comparando preços café robusta e arabica
    df_blend_M = pd.merge(df_arabica_M, df_robusta_M, on='ano_mes', suffixes=('_arabica', '_robusta'))
    df_blend_M['preco_blend'] = (df_blend_M['preco_reais_arabica'] + df_blend_M['preco_reais_robusta']) / 2

    plt.style.use('default')
    plt.gca().set_facecolor('#FDF6E3')
    plt.figure(facecolor='#FDF6E3')
    plt.plot(df_blend_M['ano_mes'], df_blend_M['preco_reais_arabica'], label='Arábica', color='#4DA8DA')
    plt.plot(df_blend_M['ano_mes'], df_blend_M['preco_reais_robusta'], label='Robusta', color='#2C3E50')
    plt.plot(df_blend_M['ano_mes'], df_blend_M['preco_blend'], label='Blend (Média)', color='#D4AF37', linestyle='--')
    plt.title('Evolução do Preço do Café (Arábica, Robusta e Blend)', fontsize=14, color='#2C3E50')
    plt.xlabel('Ano', fontsize=12, color='#2C3E50')
    plt.ylabel('Preço (R$ por 60kg)', fontsize=12, color='#2C3E50')
    plt.xticks(color='#2C3E50')
    plt.yticks(color='#2C3E50')
    plt.grid(True, color='#CCCCCC', linestyle='--', linewidth=0.5)
    plt.legend(facecolor='#FDF6E3', frameon=False)
    plt.tight_layout()
    plt.show()

def grafico3():
    #Grafico de evolução de preços diário
    df_arabica_ = df_arabica[['data', 'preco_reais']].rename(columns={'preco_reais':'preco_arabica'})
    df_robusta_ = df_robusta[['data', 'preco_reais']].rename(columns={'preco_reais':'preco_robusta'})
    df_merged = pd.merge(df_arabica_, df_robusta_, on='data', how='inner')
    df_merged['preco_blend'] = (df_merged['preco_arabica'] + df_merged['preco_robusta']) / 2
    plt.figure(figsize=(14,6))
    plt.plot(df_merged['data'], df_merged['preco_arabica'], label='Arábica', color='#2980B9')
    plt.plot(df_merged['data'], df_merged['preco_robusta'], label='Robusta', color='#2C3E50')
    plt.plot(df_merged['data'], df_merged['preco_blend'], label='Blend (Média)', color="#DCB32D")
    plt.title('Preço Diário do Café Arábica e Robusta', fontsize=16, fontweight='bold', color='#2C3E50')
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Preço (R$ por 60kg)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.gca().set_facecolor('#FDF6E3')
    plt.gcf().patch.set_facecolor('#FDF6E3')
    plt.tight_layout()
    plt.show()

def grafico4():
    #gráfico em barra do IPCA café moido de janeiro até abril
    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(10, 6), facecolor='#FDF6E3')
    sns.barplot(data=df_IPCA_cafe_acumulado, x='ano', y='IPCA_acumulado', color= '#2980B9', edgecolor='#2C3E50')
    plt.title('IPCA acumulado (jan–abr) - Café moído', fontsize=16, weight='bold', color='#2C3E50')
    plt.xlabel('Ano', fontsize=12, color='#2C3E50')
    plt.ylabel('IPCA acumulado (%)', fontsize=12, color='#2C3E50')
    for i, row in df_IPCA_cafe_acumulado.iterrows():
        plt.text(
            i, row['IPCA_acumulado'] + 0.2,
            f"{row['IPCA_acumulado']:.2f}%",
            ha='center', va='bottom',
            fontsize=10,
            color='#2C3E50'
        )
    plt.xticks(color='#2C3E50')
    plt.yticks(color='#2C3E50')
    plt.gca().set_facecolor('#FDF6E3')
    plt.tight_layout()
    plt.show()

def grafico5():
    # Gráfico de linhas referente ao poder de compra em café
    plt.figure(figsize=(14,6))
    plt.plot(df_sal_cafe['ano_mes'], df_sal_cafe['kg_cafe_arabica_compra'], label='Arábica', color='#2980B9', linewidth=1.8)
    plt.plot(df_sal_cafe['ano_mes'], df_sal_cafe['kg_cafe_robusta_compra'], label='Robusta', color='#2C3E50', linewidth=1.8)
    plt.plot(df_sal_cafe['ano_mes'], (df_sal_cafe['kg_cafe_arabica_compra'] + df_sal_cafe['kg_cafe_robusta_compra'])/2, 
            label='Blend (Média)', color='#D4AF37', linewidth=1.8)
    plt.title('Poder de Compra do Salário Mínimo em Café', fontsize=14, fontweight='bold', color='#2C3E50', pad=15)
    plt.xlabel('Data', fontsize=12, color='#2C3E50', labelpad=10)
    plt.ylabel('Kg de Café por Salário Mínimo', fontsize=12, color='#2C3E50', labelpad=10)
    plt.xticks(rotation=45, fontsize=10, color='#2C3E50')
    plt.yticks(fontsize=10, color='#2C3E50')
    plt.grid(True, linestyle='--', alpha=0.3, color='#2980B9')
    plt.legend(frameon=False, fontsize=10)
    plt.gca().set_facecolor('#FDF6E3')
    plt.gcf().set_facecolor('#FDF6E3')

    plt.tight_layout()
    plt.show()

def grafico6():
    #IPCA vs Reajuste do salario minimo
    x = np.arange(len(df_IPCA['ano']))
    cores_categoria = {
        'IPCA_cafe': '#2980B9',           
        'IPCA_geral': '#4DA8DA',          
        'IPCA_alimentacao': '#2C3E50',    
        'reajuste_salariomin': "#555AC6"  
    }
    destaque_2025 = df_IPCA['ano'] == 2025
    plt.figure(figsize=(12, 6), facecolor='#FDF6E3')
    ax = plt.gca()
    ax.set_facecolor('#FDF6E3')
    plt.bar(x - 1.5 * 0.2, df_IPCA['IPCA_cafe'], width=0.2, label='IPCA Café', 
            color=['#D4AF37' if d else cores_categoria['IPCA_cafe'] for d in destaque_2025],
            edgecolor='#2C3E50')
    plt.bar(x - 0.5 * 0.2, df_IPCA['IPCA_geral'], width=0.2, label='IPCA Geral',
            color=["#C8C338" if d else cores_categoria['IPCA_geral'] for d in destaque_2025],
            edgecolor='#2C3E50')
    plt.bar(x + 0.5 * 0.2, df_IPCA['IPCA_alimentacao'], width=0.2, label='IPCA Alimentação e Bebida',
            color=["#6E5810" if d else cores_categoria['IPCA_alimentacao'] for d in destaque_2025],
            edgecolor='#2C3E50')
    plt.bar(x + 1.5 * 0.2, df_IPCA['reajuste_salariomin'], width=0.2, label='Reajuste Salário Mínimo',
            color=["#C5B53E" if d else cores_categoria['reajuste_salariomin'] for d in destaque_2025],
            edgecolor='#2C3E50')
    plt.xticks(x, [f'{ano}*' if ano == 2025 else str(ano) for ano in df_IPCA['ano']], color='#2C3E50')
    plt.yticks(color='#2C3E50')
    plt.ylabel('porcentagem %', fontsize=12, color='#2C3E50')
    plt.xlabel('Ano', fontsize=12, color='#2C3E50')
    plt.title('Comparação IPCA vs Reajuste do Salário Mínimo', fontsize=16, weight='bold', color='#2C3E50')
    plt.suptitle('*Dados de 2025 são parciais (jan–abr)', fontsize=10, color='gray')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()
    