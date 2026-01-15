from Estrutura.src.metricas import estatisticas as funcao
import streamlit as st
import pandas as pd
import sqlite3
import base64
import plotly.express as px
from pathlib import Path


# Carregando o logo do site
logo_path = Path(__file__).parent.parent / 'style' / 'image' / 'streamlit_logo.png'
st.logo(image=logo_path, size='large')


# -------------------------------------------
# * Carregamento de um fundo animado no site
# -------------------------------------------
video_path = Path(__file__).parent.parent / 'style' / 'videos' / 'cover.mp4'
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


# ---------------------------
# * Texto ínicial da página
# ---------------------------
st.title('📦 Analisador de Produtos - Mercado Livre')
st.write(
    'Este dashboard aprensenta uma análise dos produtos mais vendidos do site do **:yellow[Mercado Livre]**, coletados diretamente  utilizando **:green[Web Scraping]** para auxiliar análises exploratórias e comparativas. Os arquivos estão salvos em um :green[**Banco de Dados**].')


# -------------------------------
# * Tabela Dinâmica de Produtos
# -------------------------------
conexao = sqlite3.connect('Estrutura/data/banco.db')
df = pd.read_sql('SELECT * FROM produtos', conexao)

# -------------------------
# * Filtros de Pesquisa
# -------------------------
tab1, tab2, tab3 = st.tabs(
    ['📦 Tabela de Produtos', '📈 Estatísticas Gerais', '📊 Gráfico Dinâmico'])
with tab1:
    st.subheader('🔍 Filtros de Pesquisa')
    st.write('Use os filtros abaixo para refinar os dados exibidos na tabela.')

    # ---------------------------------
    # * Expander contendo os filtros
    # ---------------------------------
    with st.expander('Clique aqui e aplique filtros para a tabela:', icon=':material/filter_alt:'):

        # Criação de 2 colunas
        coluna_01, coluna_02 = st.columns(2)

        with coluna_01:

            # ! Filtro de categoria
            categorias = ['Todas'] + list(sorted(df['categoria'].unique()))
            categoria_escolha = st.multiselect(
                label=':blue[▶] Categorias:',
                options=categorias,
                help=':red[➤] Categoria dos produtos (:red[Ex:] Celular, Esporte...)',
                default=st.session_state.get('categoria_filtro', []),
                key='categoria_filtro')

            # Filtrar dados pela categoria selecionada para atualizar outros filtros
            df_categoria_filtrado = df.copy()
            if categoria_escolha and 'Todas' not in categoria_escolha:
                df_categoria_filtrado = df_categoria_filtrado[df_categoria_filtrado['categoria'].isin(
                    categoria_escolha)]

            # ! Filtro de Qtd Vendas (atualizado dinamicamente)
            qtd_vendas_lista = list(
                sorted(df_categoria_filtrado['qtd_vendas'].unique()))
            qtd_vendas_escolha = st.multiselect(
                label=':blue[▶] Quantidade de Vendas:',
                help=':red[➤] Quantidade de Vendas (:red[Obs:] O valor :orange[**"Nan"**] é um valor vazio)',
                options=qtd_vendas_lista,
                default=st.session_state.get('qtd_vendas_filtro', []),
                key='qtd_vendas_filtro')

        with coluna_02:
            # ! Filtro de Vendedor (atualizado dinamicamente)
            vendedores = ['Todos'] + \
                list(sorted(df_categoria_filtrado['vendedor'].unique()))
            vendedor_index = vendedores.index(st.session_state.get(
                'vendedor_filtro', 'Todos')) if st.session_state.get('vendedor_filtro') in vendedores else 0
            vendedor_escolha = st.selectbox(
                label=':blue[▶] Vendedores:',
                options=vendedores,
                index=vendedor_index,
                key='vendedor_filtro',
                help=':red[➤] Nomes dos vendedores (:red[Ex:] Adidas, Samsung...)')

            # ! Filtro de Avaliação (atualizado dinamicamente)
            avaliacoes = list(
                sorted(df_categoria_filtrado['avaliacao'].dropna().unique()))
            avaliacao_escolha = st.multiselect(
                label=':blue[▶] Avaliações',
                options=avaliacoes,
                help=':red[➤] Avaliações dos Compradores (:red[Ex:] 4.5⭐, 5.0⭐)',
                default=st.session_state.get('avaliacao_filtro', []),
                key='avaliacao_filtro')

        # ! Filtro de Classificação (atualizado dinamicamente)
        classificacao = list(
            sorted(df_categoria_filtrado['classificacao'].dropna().unique()))

        if classificacao:
            # Validar se o valor salvo ainda existe na lista atual
            valor_salvo = st.session_state.get('classificacao_filtro', None)
            if valor_salvo and len(valor_salvo) == 2:
                # Verificar se ambos os valores existem na lista
                if valor_salvo[0] in classificacao and valor_salvo[1] in classificacao:
                    classificacao_valor_padrao = valor_salvo
                else:
                    classificacao_valor_padrao = [
                        classificacao[0], classificacao[-1]]
            else:
                classificacao_valor_padrao = [
                    classificacao[0], classificacao[-1]]

            classificacao_escolha = st.select_slider(
                label=':orange[▶] Classificação:',
                options=classificacao,
                value=classificacao_valor_padrao,
                help=':red[➤] Ordem dos produtos mais vendidos (:red[Ex:] 1°, 2°, 3°...)',
                key='classificacao_filtro'
            )
        else:
            classificacao_escolha = None

        # ! Filtro Preço Original (atualizado dinamicamente)
        precos_originais = list(
            df_categoria_filtrado['preco_original'].dropna())
        if precos_originais:
            valor_min = int(min(precos_originais))
            valor_max = int(max(precos_originais))

            # Validar se o valor salvo ainda está no intervalo
            valor_salvo = st.session_state.get('preco_original_filtro', None)
            if valor_salvo and valor_salvo[0] >= valor_min and valor_salvo[1] <= valor_max:
                preco_original_valor_padrao = valor_salvo
            else:
                preco_original_valor_padrao = (valor_min, valor_max)

            preco_original_escolha = st.slider(
                label=':red[▶] Preço Original',
                min_value=valor_min,
                max_value=valor_max,
                value=preco_original_valor_padrao,
                help=':red[➤] Referente ao :red[**Preço sem Desconto**]',
                key='preco_original_filtro'
            )
        else:
            preco_original_escolha = None

        # ! Filtro Preço Final (atualizado dinamicamente)
        precos_finais = list(df_categoria_filtrado['preco_final'].dropna())
        if precos_finais:
            valor_min = int(min(precos_finais))
            valor_max = int(max(precos_finais))

            # Validar se o valor salvo ainda está no intervalo
            valor_salvo = st.session_state.get('preco_final_filtro', None)
            if valor_salvo and valor_salvo[0] >= valor_min and valor_salvo[1] <= valor_max:
                preco_final_valor_padrao = valor_salvo
            else:
                preco_final_valor_padrao = (valor_min, valor_max)

            preco_final_escolha = st.slider(
                label=':green[▶] Preço Final',
                min_value=valor_min,
                max_value=valor_max,
                value=preco_final_valor_padrao,
                help=':red[➤] Referente ao :green[**Preço com Desconto**]',
                key='preco_final_filtro'
            )
        else:
            preco_final_escolha = None

        # --------------------------------
        # * Botão para Limpar Filtros
        # --------------------------------
        col_botao_limpar, col_botao_aplicar = st.columns(2)

        with col_botao_limpar:
            if st.button('🗑️ Limpar Filtros', use_container_width=True):

                # Limpar apenas as chaves dos filtros
                filtro_keys = ['categoria_filtro', 'qtd_vendas_filtro', 'vendedor_filtro',
                               'avaliacao_filtro', 'classificacao_filtro', 'preco_original_filtro',
                               'preco_final_filtro', 'data_filtro']

                for key in filtro_keys:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

    # -----------------------------------------
    # * Cópia do DataFrame para Estilização
    # -----------------------------------------
    # Criando uma cópia do DataFrame
    df_filtrado = df.copy()

    # * Modificações na cópia do DataFrame para ficar mais agradável visualmente
    df_filtrado['vendedor'] = df_filtrado['vendedor'].apply(
        lambda x: '❌ Não Informado' if x == 'Não Informado' else f'✅ {x}')
    df_filtrado['produto'] = df_filtrado['produto'].apply(
        lambda x: f'{x[:40]}...')
    df_filtrado['categoria'] = df_filtrado['categoria'].apply(
        lambda x: x.capitalize())
    df_filtrado['data_coleta'] = pd.to_datetime(df['data_coleta'])

    maximo = df['preco_original'].max()

    # ---------------------------------------------
    # * Aplicando os filtros na tabela estilizada
    # ---------------------------------------------
    # Filtro de Categoria
    if categoria_escolha and 'Todas' not in categoria_escolha:
        df_filtrado = df_filtrado[df_filtrado['categoria'].isin(
            [cat.capitalize() for cat in categoria_escolha])]

    # Filtro de Vendedor
    if vendedor_escolha != 'Todos':
        vendedor_formatado = '❌ Não Informado' if vendedor_escolha == 'Não Informado' else f'✅ {vendedor_escolha}'
        df_filtrado = df_filtrado[df_filtrado['vendedor']
                                  == vendedor_formatado]

    # Filtro de Classificação
    if classificacao_escolha:
        df_filtrado = df_filtrado[df_filtrado['classificacao'].between(
            classificacao_escolha[0], classificacao_escolha[1])]

    # Filtro de Preço Original
    if preco_original_escolha:
        df_filtrado = df_filtrado[df_filtrado['preco_original'].between(
            preco_original_escolha[0], preco_original_escolha[1])]

    # Filtro de Preço Final
    if preco_final_escolha:
        df_filtrado = df_filtrado[df_filtrado['preco_final'].between(
            preco_final_escolha[0], preco_final_escolha[1])]

    # Filtro de Quantidade de Vendas
    if qtd_vendas_escolha:
        df_filtrado = df_filtrado[df_filtrado['qtd_vendas'].isin(
            qtd_vendas_escolha)]

    # Filtro de Avaliação
    if avaliacao_escolha:
        df_filtrado = df_filtrado[df_filtrado['avaliacao'].isin(
            avaliacao_escolha)]

    # --------------------------
    # * DataFrame Estilizado
    # --------------------------
    df_editado = st.data_editor(
        df_filtrado,
        column_config={
            "produto": st.column_config.TextColumn(
                label="Produto", help=':red[➤] Nome dos Produtos'
            ),
            "categoria": st.column_config.TextColumn(
                label='Categoria', help=':red[➤] Categoria dos Produtos'
            ),
            "vendedor": st.column_config.TextColumn(
                label='Vendedor', help=':red[➤] Nome do Vendedor'
            ),
            "classificacao": st.column_config.NumberColumn(
                label='Classificação', format='%d° mais vendido', help=':red[➤] Classificação de Vendas'
            ),
            "qtd_vendas": st.column_config.NumberColumn(
                label='Quantidade de Vendas', format='%d Vendas 💵', help=':red[➤] Quantidade Vendida'
            ),
            "avaliacao": st.column_config.NumberColumn(
                label='Avaliação', format='%f ⭐', help=':red[➤] Avaliação dos Compradores'
            ),

            "preco_original": st.column_config.ProgressColumn(
                label='Preço Original',
                format='R$ %d',
                min_value=0,
                max_value=maximo,
                help=':red[➤] Preço :red[**antes do desconto**] ser aplicado'
            ),

            "preco_final": st.column_config.ProgressColumn(
                label='Preço Final',
                format='R$ %d',
                min_value=0,
                max_value=maximo,
                help=':green[➤] Preço :green[**depois do desconto**] ser aplicado'
            ),

            "imagem": st.column_config.ImageColumn(
                label='Imagem', help=':red[➤] Imagem do produto'
            ),
            "link": st.column_config.LinkColumn(
                label='Link', display_text='Link para o produto', help=':red[➤] Link do produto'
            ),
            "data_coleta": st.column_config.DateColumn(
                label='Data Coleta', format='DD/MM/YYYY', help=':red[➤] Data em que o dado foi coletado'
            ),
        }
    )

    # ------------------------------------------------------
    # * Expander contendo informações técnicas da tabela atual
    # ------------------------------------------------------
    with st.expander(":green[Clique] aqui e veja as :orange[**informações técnicas**] da tabela", icon=':material/dataset:'):
        # Identifica colunas categóricas (texto) e numéricas
        colunas_categoricas = df.select_dtypes(exclude='number').columns
        colunas_numericas = df.select_dtypes(include='number').columns

        # Quantidade de colunas categóricas e numéricas
        qtd_colunas_categ = len(colunas_categoricas)
        qtd_colunas_num = len(colunas_numericas)

        st.write(f'• Colunas numéricas: {qtd_colunas_num}')
        st.write(f'• Colunas categóricas: {qtd_colunas_categ}')

        # Nova tabela contendo as informações detalhadas
        st.dataframe(
            pd.DataFrame({
                "Tipos de Dados": df.dtypes.astype(str),
                "Valores Não Nulos": df.notnull().sum(),
                "Valores Nulos": df.isnull().sum()
            })
        )

        # Aviso informativo para o usuário
        with st.popover('Dica!', icon=':material/done_outline:'):
            st.info(
                'Clique no :blue[Nome das Colunas] para aplicar um filtro de ordem :green[Crescente] / :red[Decrescente].', icon=':material/warning:', )

    # -------------------------------------------------
    # * Pop-Up para detalhamento individual dos produtos
    # -------------------------------------------------
    with st.expander(':green[Clique] para acessar :red[**informações indiviuais**] de cada produto', icon=':material/info:'):

        # Seleciona um número de acordo com o ID do produto
        id_produto = st.number_input(
            label='Selecione um produto para visualizá-lo :green[**(ID do produto)**]:',
            min_value=0,
            max_value=df['produto'].count() - 1,
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
                return f"***:{cor}[{primeiras}]*** **:gray[{resto}.]**"
            elif encurtar_palavra == True:
                return f"{primeiras}"
            else:
                return f":{cor}[{primeiras}]"

        # ! Coluna 1: Imagem do produto
        with col1:
            st.image(
                df['imagem'][id_produto],
                caption=F'**Imagem: {colorir_primeiras_palavras(df["produto"][id_produto], cor="green")}.**')

        # ! Coluna 2: Informações o produto estilizadas
        with col2:
            # * ------ Nome do produto ------ #
            st.write(
                f' ▶ Nome: {colorir_primeiras_palavras(df["produto"][id_produto], cor="green", resto=True)}')

            categoria = df['categoria'][id_produto].capitalize()
            st.write(f"▶ Categoria: :blue[**{categoria}**]")

            # * ------ Vendedor ------ #
            vendedor = df['vendedor'][id_produto]
            st.write(f":red[✘ Vendedor não informado.]" if vendedor ==
                     'Não Informado' else f" ▶ Vendedor: **:orange[{vendedor}]**")

            # * ----- Classificação ------ #
            st.write(
                f" ▶ Classificação: **:red[{df['classificacao'][id_produto]}° mais vendido.]**")

            # * ----- Avaliação ----- #
            avaliacao = df['avaliacao'][id_produto]
            st.write(f" ▶ Avaliação: :yellow[{avaliacao}]⭐" if pd.notna(
                avaliacao) else f" :red[✘ O produto não possui **avaliações suficientes**.]")

            # * ----- Qtd de Vendas ----- #
            qtd_vendas = df['qtd_vendas'][id_produto]
            st.write(f" ▶ Quantidade Vendida: :orange[{int(qtd_vendas)}]" if pd.notna(
                qtd_vendas) else " :red[✘ O produto possui **poucas vendas**.]")

            # * ----- Preço final do produto ----- #
            preco_original = df['preco_original'][id_produto]
            st.write(f" ➤ Preço sem Desconto: **:blue[R${preco_original}]**" if pd.notna(
                preco_original) else " :red[✘ O produto não possui **desconto**.]")

            # * ---- Preço final com o desconto ---- #
            st.write(
                f' ➤ Preço atual: **:green[R${df["preco_final"][id_produto]}]**')

            # * ----- Botão para a página original do produto ----- #
            st.link_button('Clique para acessar o produto',
                           url=df['link'][id_produto],
                           width='stretch',
                           icon=':material/keyboard_double_arrow_right:')


with tab2:
    # -------------------------
    # * Estatísticas Gerais
    # -------------------------
    st.subheader('📈 Estatísticas Gerais')
    st.write(
        'Explore as estatísticas de cada categoria e tire suas próprias conclusões.')

    # Dicionário com o nome dos arquivos
    nome_arquivos = {
        '📱 Celular': 'Celular',
        '🖥️ Computador': 'Computador',
        '🏠 Eletrodoméstico': 'Eletrodomestico',
        '🏀 Esporte': 'Esporte',
        '📸 Informática': 'Informatica',
        '🎮 Video Game': 'Video game'
    }

    # Controle de Segmento para ficar visualmente mais facil de alterar entre as categorias
    aba = st.pills(
        label='Comparação estatística de cada categoria:',
        options=nome_arquivos,
        selection_mode='single'
    )

    # Filtrando dados pela categoria selecionada
    if aba:
        # Pega a categoria do dicionário
        categoria_selecionada = nome_arquivos[aba]
        df_metrica = df[df['categoria'].str.lower(
        ) == categoria_selecionada.lower()].copy()
    else:
        df_metrica = None

    # Criando colunas
    metrica1, metrica2, metrica3 = st.columns(3)
    metrica4, metrica5, metrica6 = st.columns(3)

    # --------------------------------
    # * Função que cria uma métrica
    # --------------------------------
    # Função que cria uma métrica personalizada

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

        # ! Quantidade de Produtos
        metrica(metrica=metrica1, titulo='Quantidade de Produtos', funcao=funcao.qtd_produtos(
            df_metrica), delta=True, valor_delta="100%", cor_delta='off')

        # ! Média de Preço sem Desconto
        metrica(metrica=metrica2, titulo='Média de Preço sem Desconto',
                funcao=f"{funcao.media_preco_original(df_metrica):.2f}")

        #  Calculando o valor entre as médias em forma de porcentagem
        df_desc = df_metrica[df_metrica['preco_final'].notna() & (
            df_metrica['preco_final'] < df_metrica['preco_original'])]

        # Média dos preços sem (media original) e com desconto (media final)
        media_original = df_desc['preco_original'].mean()
        media_final = df_desc['preco_final'].mean()
        diferenca_percentual = (
            (media_original - media_final) / media_original) * 100

        # ! Média de Preço com Desconto
        metrica(metrica=metrica3, titulo='Média de Preço com Desconto',
                funcao=f"{funcao.media_preco_final(df_metrica):.2f}", delta=True, valor_delta=f"Economia de: {diferenca_percentual:.2f}%")

        # ! Produto mais barato
        metrica(metrica=metrica4, titulo='Produto mais barato',
                funcao=funcao.produto_mais_barato(df_metrica))

        # ! Produto mais caro
        metrica(metrica=metrica5, titulo='Produto mais caro',
                funcao=funcao.produto_mais_caro(df_metrica))

        # ! Soma total de preços
        metrica(metrica=metrica6, titulo='Soma total de preços',
                funcao=funcao.soma_total(df_metrica))

    else:
        st.warning('Selecione uma categoria para ver as estatísticas.',
                   icon=':material/warning:')


# --------------------------------
# * Gráficos Dinâmicos
# --------------------------------
with tab3:
    st.subheader('📊 Gráfico Dinâmico')
    st.write('Explore as combinações das colunas e suas relações.')

    escolha = st.selectbox(
        label='Escolha uma categoria para visualizar:',
        options=['Nenhuma'] + list(nome_arquivos.keys())
    )

    # Filtra dados pela categoria selecionada para o gráfico
    if escolha == 'Nenhuma':
        st.warning('Nenhuma categoria selecionada!', icon=':material/warning:')
    else:
        categoria_grafico = nome_arquivos[escolha]
        df_grafico = df[df['categoria'].str.lower(
        ) == categoria_grafico.lower()].copy()

        coluna1, coluna2, coluna3 = st.columns(3)
        with coluna1:
            opcao1 = st.selectbox('Selecione a 1ª coluna:',
                                  df_grafico.columns.drop(['imagem', 'link']))
        with coluna2:
            opcao2 = st.selectbox('Selecione a 2ª coluna:',
                                  df_grafico.columns.drop(['imagem', 'link', opcao1]))
        with coluna3:
            orientacao = st.selectbox(
                'Orientação:', ['Horizontal', 'Vertical'], index=0)

        # Calcular altura dinâmica baseada na quantidade de dados
        altura_grafico = max(400, len(df_grafico) * 15)

        # Criar gráfico com orientação dinâmica
        if orientacao == 'Horizontal':
            grafico = px.bar(df_grafico, y=opcao1, x=opcao2, color=opcao1, orientation='h',
                             title=f'➤ Comparação entre as colunas: [{opcao1}] X [{opcao2}].',
                             text_auto=True, height=altura_grafico)
        else:
            grafico = px.bar(df_grafico, x=opcao1, y=opcao2, color=opcao1,
                             title=f'➤ Comparação entre as colunas: [{opcao1}] X [{opcao2}].',
                             text_auto=True, height=500)

        st.plotly_chart(grafico, use_container_width=True)


# * Links para acessar as outras páginas do projeto
st.divider()
st.subheader('🌐 Acesso a outras páginas')
st.write(
    ':green[**Clique**] nos botões abaixo e conheça mais sobre o Projeto!')

botao1, botao2, botao3 = st.columns(3)
with botao1:
    if st.button(':blue[***Visão Geral do Projeto***]', icon=':material/reply:', width='stretch'):
        st.switch_page('Estrutura/pages/visao_geral.py')

with botao2:
    st.link_button('★ :orange[***Repositório do Projeto***]',
                   url='https://github.com/MathGeneze/Web-Scraping-Mercado-Livre', width='stretch')


with botao3:
    if st.button(':red[***Extração de Dados***]', icon=':material/prompt_suggestion:', width='stretch'):
        st.switch_page('Estrutura/pages/web_scraping.py')
