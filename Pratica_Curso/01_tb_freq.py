 # %%

import pandas as pd
import sqlalchemy


df = pd.read_csv("../data/points_tmw.csv")

engine = sqlalchemy.create_engine("sqlite:///../data/tmw.db")

df.to_sql("points", engine, if_exists="replace", index=False)

# %%

freq_produto = df.groupby(["descProduto"])[["idTransacao"]].count()
freq_produto

# %%

freq_produto["Freq. Abs Acum."] = freq_produto["idTransacao"].cumsum()

# %%

freq_produto["Freq. Rel."] = freq_produto["idTransacao"] / freq_produto["idTransacao"].sum()

# %%

freq_produto["Freq. Rel. Acum."] = freq_produto["Freq. Rel."].cumsum()
freq_produto

# %%

df_2 = df.groupby(["descCategoriaProduto"])[["idTransacao"]].count()
df_2

# %%

df_2["Freq. Abs. Acum."] = df_2["idTransacao"].cumsum()
df_2

# %%

df_2["Freq. Rel."] = df_2["idTransacao"] / df_2["idTransacao"].sum()
df_2

# %%

df_2["Freq. Rel. Acum."] = df_2["Freq. Rel."].cumsum()
df_2
# %%
