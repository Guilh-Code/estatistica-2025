# %%

import pandas as pd

# %%

df = pd.read_csv("../data/points_tmw.csv")
df.head()

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
