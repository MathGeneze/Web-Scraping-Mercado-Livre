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
st.divider()
st.title('✅ O problema que ele resolve')
st.write('Particularmente, achei a :orange[**API**] do :yellow[**Mercado Livre**] de difícil acesso, mais especificamente dizendo sobre a parte de :orange[**Autenticação**] do próprio login, que exige documentos pessoais e simplesmente você não consegue realizar um simples login.')

st.write('O problema que o meu projeto resolveu é exatamente a :green[**coleta de dados**] de forma alternativa a uma API, extraindo os dados diretamente do site, sem precisar de chaves e requisições. Com esses dados, o acesso a insights sobre os produtos mais vendidos da Mercado Livre é facilitado com o site do :red[**Streamlit**].')


# ------------------------------
# * - Tecnologias utilizadas
# ------------------------------
st.divider()
st.title('🖥️ Tecnologias Utilizadas')
st.write('Abaixo segue a lista das tecnologias utilizadas neste projeto:')

# ! Usuário seleciona uma tecnologia e abre um card com sua descrição
tecnologia = st.selectbox('Selecione uma tecnologia e veja sua descrição:', ['Nenhum', 'Python', 'Selenium', 'Pandas', 'Streamlit', 'Plotly'], help='Abaixo contém a descrição de cada tecnologia e sua importância no projeto.')


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
st.divider()
st.title('📒 Aprendizados e Objetivos Futuros')

st.subheader('▶ O que aprendi com o projeto?')
st.write('Esse foi um projeto no qual eu aprendi que coletar dados vai muito além do que simplesmente usar uma biblioteca e extraí-los, é preciso entender a :blue[**importância do dado**], o jeito que esse dado é tratado para posteriormente gerar uma informação.')

st.subheader('▶ Ideias de Melhorias Futuras')
st.write("""
         Atualmente, o projeto possui algumas limitações, como: 
         * :red[✘ **Problema**]: Dados salvos em pastas locais do projeto;
            * :green[✔ **Solução**]: Salvar os dados em um Banco de Dados.
         * :red[✘ **Problema**]: O usuário que utilizar apenas o site, não consegue atualizar os dados;
            * :green[✔ **Solução**]: Criar um botão que rode o scrpit de extração e atualize os dados.
         """)


st.subheader('▶ Agradecimentos Finais')
st.write('Muito obrigado por visitar o meu projeto. Fique a vontade para clonar o repositório no GitHub e modificá-lo! :)')

# * Link para acessar as outras páginas do site
st.write(':red[▶] Clique nos títulos abaixo e explore mais sobre o Projeto!')
botao1, botao2, botao3 = st.columns(3)
with botao1:
    st.page_link('Estrutura/pages/main.py', label=':blue[***Análise dos Produtos***]', icon=':material/reply:', width='stretch')

with botao2:
    st.page_link('https://github.com/MathGeneze/Web-Scraping-Mercado-Livre', label='★ :orange[***Repositório do Projeto***]', width='stretch')

with botao3:
    st.page_link('Estrutura/pages/web_scraping.py', label=':red[***Extração de Dados***]', icon=':material/prompt_suggestion:', width='stretch')