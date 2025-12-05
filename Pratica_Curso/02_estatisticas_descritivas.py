# %%

import pandas as pd

# %%

df = pd.read_csv("../data/points_tmw.csv")
df.head()

# %%

variancia = df["qtdPontos"].var()
desvio_padrao = df["qtdPontos"].std()

print("Variância: ", variancia)
print("Desvio-Padrão: ", desvio_padrao)

# %%

df["qtdPontos"].describe()

# %%

usuarios = df.groupby("idUsuario").agg(
    {"idTransacao":"count",
    "qtdPontos":"sum"}
).reset_index()

usuarios

# %%

usuarios[["idTransacao", "qtdPontos"]].describe()

# %%
