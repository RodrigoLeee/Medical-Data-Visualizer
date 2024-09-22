import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
# Creating the OVERWEIGHT COLUMN
# FIRST CALCULATE BMI
df['overweight'] = df['weight'] / ((df['height'] / 100) ** 2)
# THEN APPLY THE OVERWEIGHT CONDITION
# LAMBDA é utilizado para rodar funções simples SEM TER QUE CRIAR FUNÇÕES
df['overweight'] = df['overweight'].apply(lambda x: 1 if x > 25 else 0)

# 3
# DATA NORMALIZATION
# Utiliza lambda para pequena funções
# 0 para valor igual a 1, 1 para valores maiores que 1, e o próprio valor para valores menores que 1
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1 if x > 1 else x)
# 0 para valor igual a 1, 1 para valores maiores que 1, e o próprio valor para valores menores que 1
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1 if x > 1 else x)

# 4
# CATEGORICAL PLOT
# PRIMEIRA FUNÇÃO, desenha catplot
def draw_cat_plot():
    # 5
    # Cria um NOVO DATAFRAME, com as seguintes colunas de "df"
    df_cat = pd.melt(df, id_vars=['cardio'], 
                     value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])

    # 6
    # Cria uma coluna em df_cat com TODOS OS VALORES = 1
    df_cat['total'] = 1
    # Agrupa df_cat pelas 3 colunas mencionadas
    # count() conta quantas vezes CADA VALOR aparece
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).count()    

    # 7
    # Converte os valroes DAS 3 COLUNAS MENCIONADAS para string
    df_cat['value'] = df_cat['value'].astype(str)
    df_cat['cardio'] = df_cat['cardio'].astype(str)
    df_cat['variable'] = df_cat['variable'].astype(str)

    # Cria o categorical plot com diversas configurações
    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat, kind='bar').fig   
    
    # 8
    #fig = None
    #plt.show()

    # 9
    # Salva a figura
    # Retorna a figura quando a função é chamada
    fig.savefig('catplot.png')
    return fig
    


# 10
def draw_heat_map():
    # 11
    # Cria uma copia de df em df_heat
    df_heat = df.copy()
    #
    df_heat = df_heat[
        # Compares Diastolic and Systolic blood pressure
        # is Diastolic blood pressure less than or equal to Systolic blood pressure???
        (df_heat['ap_lo'] <= df_heat['ap_hi']) &
        # Guarda dados de diversas colunas
        # Quantile é utilizado para pegar os valores de 2.5% e 97.5%
        (df_heat['height'] >= df_heat['height'].quantile(0.025)) &
        (df_heat['height'] <= df_heat['height'].quantile(0.975)) &
        (df_heat['weight'] >= df_heat['weight'].quantile(0.025)) &
        (df_heat['weight'] <= df_heat['weight'].quantile(0.975)) 
    ]

    # 12
    # Calculates the CORRELATION MATRIX of df_heat
    corr = df_heat.corr()

    # 13
    # Generates mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    # Utilizando matplotlib inicia a figura
    fig, ax = plt.subplots(figsize=(12, 12))

    # 15
    # Cria o HEATMAP    
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', cmap='RdYlBu')
    # Rotaciona labels do eixo Y
    plt.yticks(rotation=0)  

    # 16
    # Salva a figura
    fig.savefig('heatmap.png')
    # Retorna a figura quando a função é chamada
    return fig