import streamlit as st

# * Fundo animado da página
with open('Estrutura/style/style2.css') as fundo:
    st.markdown(f'<style>{fundo.read()}</style>',
        unsafe_allow_html=True)
    

# * - Introdução
# - Exemplifique o projeto em poucas linhas, sem entrar em código, foando na clareza, não na complexidade.
st.title('💡 Introdução')
st.write("""
         Este projeto é um :yellow[**ETL simples**]  (processo que envolve :orange[**Extração**], :blue[**Transformação**] e :green[**Carregamento**] de dados) separados em 2 partes:
         
         * :orange[**Parte 1**] (**Extração** e **Transformação**): O script principal extrai automaticamente dados de produtos do site da Mercado Livre. Durante a extração, o programa trata os dados e os armazena em um arquivo CSV.
         
         * :blue[**Parte 2**] (**Carregamento**): A parte de visualização desses dados acontece neste site através do :red[**Streamlit**], onde se pode ter informações detalhadas sobre esses dados. 
         """)


# * - Como o projeto funciona (fluxo geral)
# - Sem código, apenas lógica.
# - Posso usar um passo a passo ou até um fluxograma simples.
st.divider()
st.title('⚙️ Como o projeto funciona?')
st.write('Abaixo segue um fluxograma mostrando o processo de :orange[**Extração**] e :blue[**Transformação**] dos dados de um jeito simplificado.')

st.image('Estrutura/style/fluxograma.png', caption='Fluxograma mostrando o processo de Extração de Dados',)



# * - O problema que ele resolve
# - Aqui posso explicar algo como: Necessidade de automação na coleta de informações públicas;
# - Também em como é extreamamente complexo e dificil acessar a API da Mercado Livre.
st.divider()
st.title('✅ O problema que ele resolve')



# * - Tecnologias utilizadas
# - Tecnologia + o papel dela no projeto.
st.divider()
st.title('🖥️ Tecnologias Utilizadas')
st.write('Abaixo segue a lista das tecnologias utilizadas neste projeto:')

# ! Usuário seleciona uma tecnologia e abre um card com sua descrição
tecnologia = st.selectbox('Selecione uma tecnologia e veja sua descrição:', ['Nenhum', 'Python', 'Selenium', 'Pandas', 'Streamlit', 'Plotly'], help='Abaixo contém a descrição de cada tecnologia e sua importância no projeto.')







# * - Aprendizados e Objetivos Futuros
# - O que aprendi com o projeto / O que pretendo melhorar.
# - Ideias de melhorias futuras


