import streamlit as st
import pandas as pd
import base64
from pathlib import Path

st.set_page_config(layout="wide")

# -------------------------------------------
# * Carregamento de um fundo animado no site
# -------------------------------------------
video_path = Path("style/cover.mp4")
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
with open("style/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------------------
# * Texto ínicial da página
# ---------------------------
st.title('Analisador de Produtos - Mercado Livre')
st.write('Este dashboard aprensenta uma análise dos produtos mais vendidos do site da **:yellow[Mercado Livre]**, coletados diretamente  utilizando **:green[Web Scraping]** para auxiliar análises exploratórias e comparativas.')


# Lista estilizada (visível ao usuário)
lista_style = ['Nenhuma','📱 Celular','🖥️ Computador','🏠 Eletrodoméstico','🏀 Esporte','📸 Informática', '🎮 Video Game']


# Dicionário com o nome dos arquivos
nome_arquivos = {
    '📱 Celular': 'celular',
    '🖥️ Computador': 'computador',
    '🏠 Eletrodoméstico': 'eletrodomestico',
    '🏀 Esporte': 'esporte',
    '📸 Informática': 'informatica',
    '🎮 Video Game': 'video_game'
}

# -----------------------------------
# Função de Carregamento de arquivo
# -----------------------------------
def carregar_arquivo(escolha_usuario: str, dicionario: dict) -> pd.DataFrame | None:
    """
    Retorna um DataFrame com base na escolha do usuário.
    Caso a escolha seja inválida, retorna None.
    """
    if escolha_usuario not in dicionario:
        return None
    
    nome_arquivo = dicionario[escolha_usuario]
    caminho = f'./data/{nome_arquivo}.csv'
    
    return pd.read_csv(caminho)

# -------------------------------
# * Tabela Dinâmica de Produtos 
# -------------------------------
st.divider()
st.subheader('Tabela Dinâmica de Produtos')
st.write('Cada categoria representa um :orange[**Arquivo CSV**] que contém os dados mais relevantes de cada produto.')

escolha = st.selectbox(
    label='Escolha uma categoria:',
    options=['Nenhuma'] + list(nome_arquivos.keys())
)

df_tabela = carregar_arquivo(escolha, nome_arquivos)

# Se o usuário selecionar uma opção diferente de "Nenhuma", o programa vai abrir o arquivo em formato de um DataFrame
if df_tabela is not None:
    st.dataframe(df_tabela)

    # ------------------------------------------------------
    # * Expander contendo informações técnicas da tabela atual
    # ------------------------------------------------------
    with st.expander(":green[Clique] aqui e veja as :orange[**informações técnicas**] da tabela", icon=':material/dataset:'):
        # Identifica colunas categóricas (texto) e numéricas
        colunas_categoricas = df_tabela.select_dtypes(exclude='number').columns
        colunas_numericas = df_tabela.select_dtypes(include='number').columns
        # Quantidade de colunas categóricas e numéricas
        qtd_colunas_categ = len(colunas_categoricas)
        qtd_colunas_num = len(colunas_numericas)

        st.write(f'• Colunas numéricas: {qtd_colunas_num}')
        st.write(f'• Colunas categóricas: {qtd_colunas_categ}')

        # Nova tabela contendo as informações detalhadas
        st.dataframe(
            pd.DataFrame({
                "Tipos de Dados": df_tabela.dtypes,
                "Valores Não Nulos": df_tabela.notnull().sum(),
                "Valores Nulos": df_tabela.isnull().sum()
            })
        )  
        
        # Aviso informativo para o usuário
        with st.popover('Dica!', icon=':material/done_outline:'):
            st.info('Clique no :blue[Nome das Colunas] para aplicar um filtro de ordem :green[Crescente] / :red[Decrescente].', icon=':material/warning:', )
 
 
    # -------------------------------------------------
    # * Pop-Up para detalhamento individual dos produtos 
    # -------------------------------------------------
    with st.expander(':green[Clique] para acessar :red[**informações indiviuais**] de cada produto', icon=':material/info:'):
        
        # Seleciona um número de acordo com o ID do produto
        id_produto = st.number_input(
            label='Selecione um produto para visualizá-lo :green[(ID do produto)]:',
            min_value=0,
            max_value=df_tabela['produto'].count() -1,
            value=0,
            icon=':material/apps:'
        )

        # ------------------------------------------
        # * Criando uma visualização do produto 
        # ------------------------------------------
        col1, col2 = st.columns(2)
        
        # Função para estilizar a saída da string com cores
        def colorir_primeiras_palavras(texto, n=3, cor="blue", resto=False, encurtar_palavra=False):
            palavras = texto.split()
            primeiras = " ".join(palavras[:n])
            if resto == True:
                resto = " ".join(palavras[n:])
                return f"**:{cor}[{primeiras}]** **:gray[{resto}.]**"
            elif encurtar_palavra == True:
                return f"{primeiras}"
            else:
                return f":{cor}[{primeiras}]"

        
        # > Coluna 1: Imagem do produto
        with col1:
            st.image(
                df_tabela['imagem'][id_produto], 
                caption=F'**Imagem: {colorir_primeiras_palavras(df_tabela["produto"][id_produto], cor="green")}.**')
        
        # > Coluna 2: Informações o produto estilizadas
        with col2:
             # * --- Nome do produto --- #
            st.write(f' ▶ Nome: {colorir_primeiras_palavras(df_tabela["produto"][id_produto], cor="green", resto=True)}')

            # * --- Vendedor --- #
            vendedor = df_tabela['vendedor'][id_produto]
            st.write(f":red[✘ Vendedor não informado.]" if vendedor == 'Não Informado' else f" ▶ Vendedor: **:orange[{vendedor}]**")
            
            # * --- Classificação --- #
            st.write(f" ▶ Classificação: **:red[{df_tabela['classificacao'][id_produto]}° mais vendido.]**")
            
            # * --- Avaliação --- # 
            avaliacao = df_tabela['avaliacao'][id_produto]
            st.write(f" ▶ Avaliação: :yellow[{avaliacao}]⭐" if pd.notna(avaliacao) else f" :red[✘ O produto não possui **avaliações suficientes**.]" )

            # * --- Qtd de Vendas --- # 
            qtd_vendas = df_tabela['qtd_vendas'][id_produto]
            st.write(f" ▶ Quantidade Vendida: :orange[{int(qtd_vendas)}]" if pd.notna(qtd_vendas) else " :red[✘ O produto possui **poucas vendas**.]")

            # * --- Preço final do produto --- #  
            preco_original = df_tabela['preco_original'][id_produto]
            st.write(f" ➤ Preço sem Desconto: **:blue[R${preco_original}]**" if pd.notna(preco_original) else " :red[✘ O produto não possui **desconto**.]")
                
            # * --- Preço final com o desconto --- # 
            st.write(f' ➤ Preço atual: **:green[R${df_tabela["preco_final"][id_produto]}]**')
            
            # * --- Botão para a página original do produto --- # 
            st.link_button('Clique para acessar o produto', url=df_tabela['link'][id_produto], width='stretch')
    
    
# -------------------------
# * Estatísticas Gerais 
# -------------------------
from src.metricas import estatisticas as funcao

st.divider()
st.subheader('Estatísticas Gerais')
st.write('Explore as estatísticas de cada categoria e tire suas próprias conclusões.')

# Controle de Segmento para ficar visualmente mais facil de alterar entre as categorias
aba = st.pills(
    label='Comparação estatística de cada categoria:',
    options=nome_arquivos,
    selection_mode='single'
)

# Carregando o arquivo 
df_metrica = carregar_arquivo(aba, nome_arquivos)

# Criando colunas 
metrica1, metrica2, metrica3 = st.columns(3)
metrica4, metrica5, metrica6 = st.columns(3)

# --------------------------------
# * Função que cria uma métrica
# --------------------------------
def metrica(metrica, titulo, funcao, delta=False, valor_delta=0, cor_delta='normal'):
    with metrica:
        if delta == False:
            st.metric(
                label=titulo,
                value=funcao,
                border=True
            )
        else:
            st.metric(
                label=titulo,
                value=funcao,
                delta=valor_delta,
                delta_color=cor_delta,
                border=True
            )  
            

if df_metrica is not None:
    metrica(metrica=metrica1, titulo='Quantidade de Produtos', funcao=funcao.qtd_produtos(df_metrica), delta=True, valor_delta="100%", cor_delta='off')
    metrica(metrica=metrica2, titulo='Média de Preço sem Desconto', funcao=f"{funcao.media_preco_original(df_metrica):.2f}")
    
    # * Calculando o valor entre as médias em forma de porcentagem
    df_desc = df_metrica[df_metrica['preco_final'].notna() & (df_metrica['preco_final'] < df_metrica['preco_original'])]
    media_original = df_desc['preco_original'].mean()
    media_final = df_desc['preco_final'].mean()
    
    diferenca_percentual = ((media_original - media_final) / media_original) * 100
    metrica(metrica=metrica3, titulo='Média de Preço com Desconto', funcao=f"{funcao.media_preco_final(df_metrica):.2f}", delta=True, valor_delta=f"Economia de: {diferenca_percentual:.2f}%")
    
    metrica(metrica=metrica4, titulo='Produto mais barato', funcao=funcao.produto_mais_barato(df_metrica))
    metrica(metrica=metrica5, titulo='Produto mais caro', funcao=funcao.produto_mais_caro(df_metrica))
    metrica(metrica=metrica6, titulo='Soma total de preços', funcao=funcao.soma_total(df_metrica))

else:
    st.info('Selecione uma categoria para ver as estatísticas.')


# --------------------------------
# * Gráficos Dinâmicos
# --------------------------------
import plotly.express as px

st.divider()
st.subheader('Gráfico Dinâmico')
st.write('Explore as combinações das colunas e suas relações.')

escolha = st.selectbox(
    label='Escolha uma categoria para visualizar:',
    options=['Nenhuma'] + list(nome_arquivos.keys())
)

# Usuário seleciona ua categoria para visualizar o gráfico
df_grafico = carregar_arquivo(escolha, nome_arquivos)

if escolha == 'Nenhuma':
    st.info('Nenhuma coluna selecionada.')
else:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        opcao1 = st.selectbox('Selecione a 1ª coluna:', df_grafico.columns.drop(['imagem', 'link']))
    with coluna2:
        opcao2 = st.selectbox('Selecione a 2ª coluna:', df_grafico.columns.drop(['imagem', 'link', opcao1]))

    
    grafico = px.bar(df_grafico, x=opcao1, y=opcao2, color=opcao1, title=f'➤ Comparação entre as colunas: [{opcao1}] X [{opcao2}].', text_auto=True)
    
    st.plotly_chart(grafico)
