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



# -----------------------
# * Extração de Dados
# -----------------------
st.title('📤 Extração de Dados')
st.write('Abaixo ressaltarei as partes mais relevântes do código para melhor entendimento.')


# * Link para acessar as outras páginas do site
st.write(':red[▶] Clique nos títulos abaixo e explore mais sobre o Projeto!')
botao1, botao2, botao3 = st.columns(3)
with botao1:
    st.page_link('Estrutura/pages/main.py', label=':blue[***Análise dos Produtos***]', icon=':material/reply:', width='stretch')

with botao2:
    st.page_link('https://github.com/MathGeneze/Web-Scraping-Mercado-Livre', label='★ :orange[***Repositório do Projeto***]', width='stretch')

with botao3:
    st.page_link('Estrutura/pages/visao_geral.py', label=':red[***Visão Geral do Projeto***]', icon=':material/prompt_suggestion:', width='stretch')

# -------------------------------
# * Parâmetros das categorias
# -------------------------------
st.divider()
st.subheader('🌐 Parâmetros das categorias')
st.write('De início, importante reassaltar que o script entra em categorias pré-definidas de :orange[**Produtos mais Vendidos**] da :yellow[***Mercado Livre***] de forma automatizada. Uma forma prática de acessá-las é através dos parâmetros de cada categoria.')

st.write('Observe na imagem abaixo que no final da URL do site, existe uma espécie de :red[**código de identificação**] da categoria, que na verdade é o parâmetro dela.')

st.image('Estrutura/style/categoria.png', '*Imagem da categoria de eletrodomésticos*')

st.html('<br>')
st.write('Então criei um dicionário com o :green[**Nome da Categoria**] :red[**+**] o :green[**Parâmetro da Categoria**]. O script percorrerá esse dicionário e assim que terminar de extrair os dados da primeira categoria, irá para segunda e assim sucessivamente.')

st.markdown("""   
```python
# --------------------------------------------------------------
# Chave: nomes de categorias de produtos
# Valor: parâmetro do site da mercado livre que redireciona para a categoria
# ---------------------------------------------------------------
codigos_paginas = {
    'eletrodomestico': 'MLB5726',
    'celular': 'MLB1055',
    'computador': 'MLB1652',
    'esporte': 'MLB1276',
    'informatica': 'MLB1648',
    'video_game': 'MLB186456'
}
""", help='Trecho do código com os parâmetros do site')



# ---------------------
# * Elementos e XPATH
# ---------------------
st.divider()
st.title('🛣️ Elementos e XPATH')
st.write('Próximo passo é extrair os dados através do conceito de :orange[**XPATH**], que basicamente, é um :orange[**Identificador de Elementos do Site**]. Apartir dele, conseguimos identificar o caminho que leva até a informação que buscamos. Confira abaixo os tipos de dados extraídos.')

# * Video de apresentação dos dados
col1, col2 = st.columns(2)
with col1:
    st.video('Estrutura/style/videos/elementos.mp4', autoplay=True, loop=True)
    

# * Lista dos dados extraídos
with col2:
    st.write("""
        ```python
        # Lista de dados extraídos:
        * Imagem + Link do produto;
        * Classificação (1° mais vendido...);
        * Nome do produto;
        * Vendedor;
        * Avaliação + Qtd de vendas
        * Preço sem desconto;
        * Preço com desconto (se tiver).
             """)

st.html('<br>')
st.write('Apartir desssas informações, criei uma :blue[**função**] para :blue[**padronizar a extração de dados**], priorizando sempre um código limpo, legível para futuras manutenções. Código da função abaixo:')

st.markdown("""
    ```python
    # -----------------------------------------------
    # Função que extrai os dados de cada produto
    # -----------------------------------------------
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
            """)



# -----------------------------
# * Armazenamento dos dados
# -----------------------------
st.divider()
st.title('🗄️ Armazenamento dos dados')
st.write('Após o script extrair os dados de todos os produtos de uma determinada categoria, ele os armazena em uma :green[**lista-dicionário**], convertendo-a para um :green[**arquivo CSV**].')

st.markdown("""
    ```python
    # -----------------------------
# Loop principal
# Acessa o site, scrolla para o final da página, extrai os dados e
# salva em um dicionário
# -----------------------------
for chave, valor in codigos_paginas.items():

    # Acessa o site da Mercado livre
    drive.get(f"https://www.mercadolivre.com.br/mais-vendidos/{valor}")
    sleep(3)

    # Seleciona cards
    produtos = drive.find_elements(By.XPATH, "//li[contains(@class, 'ui-search-layout__item')]")

    dados = []

    # Loop para extrair os dados dos produtos
    for item in produtos:
        nome = extrair(item, ".//a")
        vendedor = extrair(item, ".//span[contains(@style, 'color:#191919')]")
        classificacao = extrair(item, ".//span[@style='color:#FFFFFF;background-color:#FF7733']")
        ...

        # Os dados são adicionados em uma lista-dicionário
        dados.append({
            "produto": nome,
            "vendedor": vendedor if vendedor is not None else "Não Informado",
            "classificacao": int(classificacao.replace("º MAIS VENDIDO", "")),
            ...
        })
            """)



# ---------------------
# * Código Completo
# ---------------------
st.divider()
st.title('📄 Código Completo')
st.write('Abaixo contém o :red[**código completo**] do script de extração.')

st.markdown("""
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date
from time import sleep
import pandas as pd
import sqlite3


# ----------------------------------------------------------------
# Chave: nomes de categorias de produtos
# Valor: parâmetro do site da mercado livre que redireciona para a categoria
# ----------------------------------------------------------------
codigos_paginas = {
    'eletrodomestico': 'MLB5726',
    'celular': 'MLB1055',
    'computador': 'MLB1652',
    'esporte': 'MLB1276',
    'informatica': 'MLB1648',
    'video_game': 'MLB186456'
}

drive = webdriver.Chrome()


# -----------------------------------------------
# Função que retorna os dados de cada produto
# -----------------------------------------------
def extrair(item, xpath, atributo=None):
    '''
    Retorna o texto ou atributo do elemento.
    Se nada for encontrado, retorna "" (string vazia).
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


# ----------------------------------------------------------------
# Loop principal
# Acessa o site, scrolla para o final da página, extrai os dados e     salva em um dicionário
# ----------------------------------------------------------------
for chave, valor in codigos_paginas.items():

    print(f"\n>>> Coletando categoria: {chave} ...")

    # Acessa o site da Mercado livre
    drive.get(f"https://www.mercadolivre.com.br/mais-vendidos/{valor}")
    sleep(5)

    # Carrega mais conteúdo scrollando
    actions = ActionChains(drive)
    for _ in range(12):
        actions.scroll_by_amount(0, 1200).perform()

    # Seleciona cards
    produtos = drive.find_elements(
        By.XPATH, "//li[contains(@class, 'ui-search-layout__item')]")
    
    dados = []

    # Loop para extrair os dados dos produtos
    for item in produtos:
        nome = extrair(item, ".//a")
        vendedor = extrair(item, ".//span[conta(@style'color:#191919')]")
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
            "categoria": chave,
            "vendedor": vendedor if vendedor is not None else "Não Informado",
            "classificacao": int(classificacao.replace("º MAIS VENDIDO", "")) if classificacao else None,
            "qtd_vendas": int(qtd_vendas) if qtd_vendas else None,
            "avaliacao": avaliacao,
            "preco_original": float(preco_original.replace(".", "")) if preco_original is not None else None,
            "preco_final": float(preco_final.replace(".", "")) if preco_final is not None else None,
            "imagem": imagem,
            "link": link,
            'data_coleta': date.today()
        })

    # Os dados são salvos em um Dataframe, convertidos para csv e salvos no banco de dados
    df = pd.DataFrame(dados)
    df.to_csv(f"Estrutura/data/files/{chave}.csv", index=False, encoding="utf-8")

    # * Criando a conexão com o banco de dados para salva-los
    conn = sqlite3.connect('Estrutura/data/banco.db')
    df.to_sql('produtos', conn, if_exists='append', index=False)
    conn.close()
    
    print(f"✔ {len(df)} itens salvos em {chave}.csv e na tabela 'produtos' do banco de dados")
    sleep(2.5)

drive.quit()

print("\nTodas as categorias foram coletadas com sucesso!")


""")

