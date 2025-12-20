import pandas as pd

# Quantidade de produtos
def qtd_produtos(df: pd.DataFrame):
    return len(df)

# Média de Preço antes do desconto
def media_preco_original(df: pd.DataFrame) -> float:
    media = df['preco_original'].mean()
    return media

# Média de Preço com desconto
def media_preco_final(df: pd.DataFrame) -> float:
    preco_desconto = df['preco_final'].mean()
    return preco_desconto

# -------------------------------------------
# * Produtos mais caros e baratos
# -------------------------------------------
# Produto mais caro
def produto_mais_caro(df: pd.DataFrame) -> float:
    produto = df['preco_final'].max()
    return produto

# Produto mais barato
def produto_mais_barato(df: pd.DataFrame) -> float:
    produto = df['preco_final'].min()
    return produto

# Soma de todos os preços
def soma_total(df: pd.DataFrame) -> float:
    produto = df['preco_final'].sum()
    return produto
