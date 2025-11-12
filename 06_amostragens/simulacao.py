# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_sellers = pd.read_csv("../data/olist_sellers_dataset.csv")
df_order_items = pd.read_csv("../data/olist_order_items_dataset.csv")

# %%

df_join = df_order_items.merge(df_sellers, on='seller_id')
df_join = df_join[['seller_id', 'price', 'seller_state']]
df_groupby = (df_join.groupby(["seller_id", 'seller_state'])
                     .agg(["count", "mean", "sum"])
                     .reset_index()
                     )

# %%
df_groupby.columns = ["vendedor", "estado", "quantidade", "ticket_medio", "renda_total"]
df_groupby

# %%

x = plt.boxplot(df_groupby['renda_total'])
threshold = x['fliers'][0].get_data()[-1].min()

df_groupby = df_groupby[df_groupby['renda_total']<threshold]


# %%

media_pop = df_groupby['renda_total'].mean()
print(f"Média populacional: R${media_pop:.2f}")

# %%

# AMOSTRA ALEATÓRIA SIMPLES

# Amostra de tamanho 5% (154)
n = int(df_groupby.shape[0]*0.10)

def simula_simples(iter, n, df):
    medias_amostras = []
    for i in range(iter):
        df_sample = df.sample(n)
        medias_amostras.append(df_sample['renda_total'].mean())

    return np.mean(medias_amostras), np.std(medias_amostras)

print(simula_simples(1000,n, df_groupby))

# %%



def amostra_estratificada(df, estados:pd.DataFrame):
    
    df_new = estados.copy()
    
    medias_estados = []
    
    for i in estados['estado']:
        n_estado = estados[estados['estado']==i]['n'].iloc[0]
        amostra_estado = df[df['estado']==i].sample(n_estado)
        media_estado = amostra_estado['renda_total'].mean()
        medias_estados.append(media_estado)
        
    df_new['media'] = medias_estados
    df_new['media_ponderada'] = df_new['media'] * df_new['peso']
    return df_new['media_ponderada'].sum()


def simula_estratificada(iter:int, n:int, df:pd.DataFrame):
    estados = (df.groupby("estado")
                 .agg({"vendedor":"count", "renda_total":['mean','std']})
                 .reset_index())

    estados['peso'] = estados['vendedor'] / estados['vendedor'].sum()
    estados['n'] = (estados['peso'] * n).astype(int)
    estados['n'] = estados['n'].apply(lambda x: x if x > 0 else x+1)
    medias_amostras_estratificadas = [amostra_estratificada(df, estados) for i in range(iter)]
    return np.mean(medias_amostras_estratificadas), np.std(medias_amostras_estratificadas)

# %%

ns = [50,150,300,500,750,1000,1500,2000]

data = []
for i in ns:
    
    print(f"Executando n={i}...")
    
    simples = simula_simples(1000, i, df_groupby)
    d = {
        "tipo":"simples",
         "n":i,
         "media": simples[0],
         "std":simples[1],
         }
    data.append(d)
        
    estratificada = simula_estratificada(1000, i, df_groupby)
    d = {
        "tipo":"estratificada",
         "n":i,
         "media": estratificada[0],
         "std":estratificada[1],
         }
    data.append(d)
    
# %%

df_results = pd.DataFrame(data)
df_results

df_simples = df_results[df_results['tipo']=='simples']
plt.plot(df_simples['n'],df_simples['media'])
plt.fill_between(
    df_simples['n'],
    df_simples['media'] + df_simples['std'],
    df_simples['media'] - df_simples['std'],
    alpha=0.2)

df_estratificada = df_results[df_results['tipo']=='estratificada']
plt.plot(df_estratificada['n'],df_estratificada['media'])
plt.fill_between(
    df_estratificada['n'],
    df_estratificada['media'] + df_estratificada['std'],
    df_estratificada['media'] - df_estratificada['std'],
    alpha=0.25)

plt.grid(True)
plt.xlabel("Tamanho de Amostra")
plt.ylabel("Valor de $\\bar{x}$")
plt.title("Comparação Amostra Aleatória Simples vs Estratificada")
plt.legend(["Média Simples", "Std. Simples", "Média Estratificada", "Std. Estratificada"])
plt.show()
# %%

estados = (df_groupby.groupby("estado")
                 .agg({"vendedor":"count", "renda_total":['mean','std']})
                 .reset_index())

estados