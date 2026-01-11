import streamlit as st
from pathlib import Path
import base64

# -------------------------------------------
# * Carregamento de um fundo animado no site
# -------------------------------------------
video_path = Path(__file__).parent.parent / 'style' / 'videos' / 'web.mp4'
with open(video_path, "rb") as video_file:
    video_bytes = video_file.read()
    video_base64 = base64.b64encode(video_bytes).decode()

# HTML do vídeo
video_html = f"""
<video autoplay loop muted playsinline id="video-background">
    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
</video>
<div id="video-overlay"></div>
"""

st.markdown(video_html, unsafe_allow_html=True)

#  Leitura do Arquivo CSS
css_path = Path(__file__).parent.parent / 'style' / 'style.css'
with open(css_path, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



# Nesta página, vou mostrar o código que usei para extraír os dados e explicar o processo de extração.

# Pensando em colocar gifs ou videos mostrando como é realizado esse processo de maneira dinâmica, prendendo o usuário e o conectando com a página
st.title('📤 Extração de Dados')

st.subheader('Parâmetros dos sites')
st.write('Os parâmetros')
st.markdown("""
            
```python
from selenium import webdriver

# -----------------------------
# Chave: nomes de categorias de produtos
# Valor: parâmetro do site da mercado livre que redireciona para a categoria
# -----------------------------
codigos_paginas = {
    'eletrodomestico': 'MLB5726',
    'celular': 'MLB1055',
    'computador': 'MLB1652',
    'esporte': 'MLB1276',
    'informatica': 'MLB1648',
    'video_game': 'MLB186456'
}

drive = webdriver.Chrome()

""")





st.divider()
st.title('📄 Código Completo')
st.write('Abaixo contém o código completo do script de extração.')

st.markdown("""
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd

# -----------------------------
# Chave: nomes de categorias de produtos
# Valor: parâmetro do site da mercado livre que redireciona para a categoria
# -----------------------------
codigos_paginas = {
    'eletrodomestico': 'MLB5726',
    'celular': 'MLB1055',
    'computador': 'MLB1652',
    'esporte': 'MLB1276',
    'informatica': 'MLB1648',
    'video_game': 'MLB186456'
}

drive = webdriver.Chrome()

# -----------------------------
# Função que retorna os dados de cada produto
# -----------------------------
def extrair(item, xpath, atributo=None):
    '''
    Retorna o texto ou atributo do elemento.
    Se nada for encontrado, retorna '' (string vazia).
    '''
    try:
        elemento = item.find_element(By.XPATH, xpath)
        
        # --- Se o parâmetro "atributo" for informado, a função extrairá o atributo do elemento (imagem ou link do produto), se não, retornará o texto do elemento --- #
        if atributo:
            return elemento.get_attribute(atributo) or None
        return elemento.text or None
    except:
        return None

# Função que trata os dados do N° de vendas e retorna um valor limpo
def limpar_vendas(texto):
    '''Limpa numero de vendas e retorna valor padronizado.'''
    if not texto:
        return ""
    return (texto.replace("|", "")
                 .replace("+", "")
                 .replace("vendidos", "")
                 .replace("vendido", "")
                 .replace("mil", "")
                 .replace('M', "")
                 .strip())


# -----------------------------
# Loop principal
# Acessa o site, scrolla para o final da página, extrai os dados e
# salva em um dicionário
# -----------------------------
for chave, valor in codigos_paginas.items():

    print(f"\n>>> Coletando categoria: {chave} ...")

    # Acessa o site da Mercado livre
    drive.get(f"https://www.mercadolivre.com.br/mais-vendidos/{valor}")
    sleep(3)

    # Carrega mais conteúdo scrollando
    actions = ActionChains(drive)
    for _ in range(12):
        actions.scroll_by_amount(0, 1200).perform()

    # Seleciona cards
    produtos = drive.find_elements(By.XPATH, "//li[contains(@class, 'ui-search-layout__item')]")

    dados = []

    # Loop para extrair os dados dos produtos
    for item in produtos:
        nome = extrair(item, ".//a")
        vendedor = extrair(item, ".//span[contains(@style, 'color:#191919')]")
        classificacao = extrair(item, ".//span[@style='color:#FFFFFF;background-color:#FF7733']")
        qtd_vendas = limpar_vendas(extrair(item, ".//span[contains(@class, 'poly-phrase-label')][2]"))
        avaliacao = extrair(item, ".//span[@class='poly-phrase-label'][1]")
        preco_original = extrair(item, ".//s//span[@class='andes-money-amount__fraction']")
        preco_final = extrair(item, ".//div[@class='poly-price__current']//span[@class='andes-money-amount__fraction']")
        imagem = extrair(item, ".//div[@class='poly-card__portada']/img", atributo="src")
        link = extrair(item, ".//a[contains(@class, 'poly-component__title')]", atributo="href")

        # Os dados são adicionados em uma lista-dicionário
        dados.append({
            "produto": nome,
            "vendedor": vendedor if vendedor is not None else "Não Informado",
            "classificacao": int(classificacao.replace("º MAIS VENDIDO", "")),
            "qtd_vendas": int(qtd_vendas),
            "avaliacao": avaliacao,
            "preco_original": float(preco_original.replace(".","")) if preco_original is not None else preco_original,
            "preco_final": float(preco_final.replace(".","")),
            "imagem": imagem,
            "link": link
        })

    # Os dados são salvos em um Dataframe e convertidos para csv
    df = pd.DataFrame(dados)
    df.to_csv(f"./Mercado Livre/data/{chave}.csv", index=False, encoding="utf-8")

    print(f"✔ {len(df)} itens salvos em {chave}.csv")

    sleep(2)

print("\nTodas as categorias foram coletadas com sucesso!")

""")

