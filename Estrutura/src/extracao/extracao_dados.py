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
    """
    Retorna o texto ou atributo do elemento.
    Se nada for encontrado, retorna "" (string vazia).
    """
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
    """Limpa numero de vendas e retorna valor padronizado."""
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
    sleep(7)

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
        vendedor = extrair(item, ".//span[contains(@style, 'color:#191919')]")
        classificacao = extrair(
            item, ".//span[@style='color:#FFFFFF;background-color:#FF7733']")
        qtd_vendas = limpar_vendas(
            extrair(item, ".//span[contains(@class, 'poly-phrase-label')][2]"))
        avaliacao = extrair(item, ".//span[@class='poly-phrase-label'][1]")
        preco_original = extrair(
            item, ".//s//span[@class='andes-money-amount__fraction']")
        preco_final = extrair(
            item, ".//div[@class='poly-price__current']//span[@class='andes-money-amount__fraction']")
        imagem = extrair(
            item, ".//div[@class='poly-card__portada']/img", atributo="src")
        link = extrair(
            item, ".//a[contains(@class, 'poly-component__title')]", atributo="href")

        # Os dados são adicionados em uma lista-dicionário
        dados.append({
            "produto": nome,
            "categoria": chave,
            "vendedor": vendedor if vendedor is not None else "Não Informado",
            "classificacao": int(classificacao.replace("º MAIS VENDIDO", "")) if classificacao else None,
            "qtd_vendas": int(qtd_vendas) if qtd_vendas else None,
            "avaliacao": avaliacao if isinstance(avaliacao, float) else None,
            "preco_original": float(preco_original.replace(".", "")) if preco_original is not None else None,
            "preco_final": float(preco_final.replace(".", "")) if preco_final is not None else None,
            "imagem": imagem,
            "link": link,
            'data_coleta': pd.to_datetime(date.today())
        })

    # Os dados são salvos em um Dataframe, convertidos para csv e salvos no banco de dados
    df = pd.DataFrame(dados)

    # * Criando a conexão com o banco de dados para salva-los
    conn = sqlite3.connect('Estrutura/data/banco.db')
    df.to_sql('produtos', conn, if_exists='append', index=False)
    conn.close()

    print(
        f"✔ {len(df)} itens salvos em {chave}.csv e na tabela 'produtos' do banco de dados")
    sleep(2.5)

drive.quit()

print("\nTodas as categorias foram coletadas com sucesso!")
