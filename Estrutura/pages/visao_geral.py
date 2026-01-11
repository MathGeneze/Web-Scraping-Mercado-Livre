import streamlit as st
import base64
from pathlib import Path

# * Fundo animado da página
style_path = Path(__file__).parent.parent / 'style' / 'style2.css'
with open(style_path) as fundo:
    st.markdown(f'<style>{fundo.read()}</style>',
                unsafe_allow_html=True)


# ------------------
# * - Introdução
# ------------------
st.title('💡 Introdução')
st.write("""
         Este projeto é um :yellow[**ETL simples**]  (processo que envolve :orange[**Extração**], :blue[**Transformação**] e :green[**Carregamento**] de dados) separados em 2 partes:
         
         * :orange[**Parte 1**] (**Extração** e **Transformação**): O script principal extrai automaticamente dados de produtos do site da Mercado Livre. Durante a extração, o programa trata os dados e os armazena em um arquivo CSV.
         
         * :blue[**Parte 2**] (**Carregamento**): A parte de visualização desses dados acontece neste site através do :red[**Streamlit**], onde se pode ter informações detalhadas sobre esses dados. 
         """)


# ---------------------------------------------
# * - Como o projeto funciona (fluxo geral)
# ---------------------------------------------
st.divider()
st.title('⚙️ Como o projeto funciona?')
st.write(
    'Abaixo segue um fluxograma mostrando o processo de :orange[**Extração**] e :blue[**Transformação**] dos dados de um jeito simplificado.')

# ! Expander para o usuário visualizar o fluxograma
with st.expander('Clique aqui para ver o Fluxograma do programa:', icon=':material/graph_2:'):
    image_path = Path(__file__).parent.parent / 'style' / 'fluxograma.png'
    st.image(str(image_path),
             caption='Fluxograma mostrando o processo de Extração de Dados',)


# ----------------------------------
# * - O problema que ele resolve
# ----------------------------------
# - Aqui posso explicar algo como: Necessidade de automação na coleta de informações públicas;
# - Também em como é extreamamente complexo e dificil acessar a API da Mercado Livre.
st.divider()
st.title('✅ O problema que ele resolve')


# ------------------------------
# * - Tecnologias utilizadas
# ------------------------------
# - Tecnologia + o papel dela no projeto.
st.divider()
st.title('🖥️ Tecnologias Utilizadas')
st.write('Abaixo segue a lista das tecnologias utilizadas neste projeto:')

# ! Usuário seleciona uma tecnologia e abre um card com sua descrição
tecnologia = st.selectbox('Selecione uma tecnologia e veja sua descrição:', [
                          'Nenhum', 'Python', 'Selenium', 'Pandas', 'Streamlit', 'Plotly'], help='Abaixo contém a descrição de cada tecnologia e sua importância no projeto.')

coluna1, coluna2 = st.columns(2)
if tecnologia != 'Nenhum':
    with coluna1:
        icon_path = Path(__file__).parent.parent / 'style' / \
            'icons' / f'{tecnologia.lower()}.png'
        st.image(str(icon_path), f'*Imagem do {tecnologia}*')

    with coluna2:
        font_path = Path(__file__).parent.parent / 'fonts' / \
            f'{tecnologia.lower()}.txt'
        with open(font_path, 'r', encoding='utf-8') as leitura:

            def texto_colorido(texto):
                if texto == 'Python':
                    cor = 'yellow'
                elif texto == 'Selenium':
                    cor = 'green'
                elif texto == 'Pandas':
                    cor = 'blue'
                elif texto == 'Streamlit':
                    cor = 'red'
                elif texto == 'Plotly':
                    cor = 'orange'
                st.subheader(f'Pra que serve o :{cor}[{texto}]?')

            texto_colorido(tecnologia)
            st.write(leitura.read())

else:
    st.warning('Nenhuma tecnologia selecionada!', icon=':material/info:')


# ----------------------------------------
# * - Aprendizados e Objetivos Futuros
# ----------------------------------------
# - O que aprendi com o projeto / O que pretendo melhorar.
# - Ideias de melhorias futuras
