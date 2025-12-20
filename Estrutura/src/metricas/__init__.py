import pandas as pd

# Quantidade de produtos
def qtd_produtos(df: pd.DataFrame):
    return len(df)

# Média de Preço antes do desconto
def media_preco_original(df: pd.DataFrame) -> float:
    preco_original = df['preco_original'].mean()
    return f"{preco_original:.2f}"

# Média de Preço com desconto
def media_preco_desconto(df: pd.DataFrame) -> float:
    preco_desconto = df['preco_desconto'].mean()
    return f"{preco_desconto:.2f}"

# Produto mais caro
def produto_mais_caro(df: pd.DataFrame) -> float:
    produto = df['preco_final']
    return f"{produto:.2f}"
