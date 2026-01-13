import streamlit as st

# Páginas do projeto
pages = {
    "Principal": [
        st.Page('Estrutura/pages/main.py', title='Analisador de Produtos', url_path='main', icon=':material/tab:'),
        
        st.Page('Estrutura/pages/extracao.py', title='Extrair os Dados', url_path='extracao', icon=':material/key:')
    ],
    "Visão Geral": [
        st.Page('Estrutura/pages/visao_geral.py', title='Sobre o projeto', url_path='home', icon=':material/home:'),
        
        st.Page('Estrutura/pages/web_scraping.py', title='Extração de Dados', url_path='web_scraping', icon=':material/settings:')
        
        
    ]
}

pg = st.navigation(pages)
pg.run()
