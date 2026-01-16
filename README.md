# Web Scraping - Mercado Livre
Coletor e Analisador de Dados da Mercado Livre com Python, Selenium e Streamlit.

<br>

<!----------- 📁 Sumário ---------->
## 📁 Sumário
- [Projeto](#projeto)
- [Objetivo](#objetivo)
- [Principais Tecnologias](#principais-tecnologias)
- [Funcionalidades](#funcionalidades)
- [Funcionamento do Script de Extração](#funcionamento-do-script-de-extração)
- [Como executar - Passo a Passo](#como-executar---passo-a-passo)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Imagens do Projeto](#imagens-do-projeto)
- [Aprendizados](#aprendizados)
  
<br>

<!----------- 📌 Projeto ---------->
## <a id="projeto">📌 Projeto</a>
Este projeto é separado em 2 partes: 
  * Scrpit que extrai e limpa os dados dos produtos mais vendidos da Mercado Livre em categorias específicas.
  * Interface visual que permite o usuário explorar os dados com Tabelas, Estatísticas e Gráficos.

<br>

<!----------- 🔓 Objetivo ---------->
## <a id="objetivo">🔓 Objetivo</a>
O objetivo deste projeto inicialmente era utilizar a API da Mercado Livre para acessar dados dos produtos mais vendidos e criar uma análise a partir disso, porém, particularmente tive dificuldades de acessar essa API por conta do aumento da segurança do site. Então, extraí os dados de maneira automatizada utilizando o conceito de Web Scraping (Extração de Dados) e os salvando em um Banco de Dados.

### ▶ Qual problema ele resolve?
Este projeto resolve o problema de Extração de Dados via API, poupando tempo de ler e entender a documentação, que as vezes para um iniciante, pode ser bem complexa.

### ▶ Em qual contexto ele é útil?
Ele é útil para Engenhereiros de Dados na parte de extração, podendo coletar os dados dos produtos facilmente e para Analistas de Dados, utilizando a interface visual para tirar insights valiosos sobre os produtos.

<br>

<!----------- 🖥️ Principais Tecnologias ---------->
## <a id="principais-tecnologias">🖥️ Principais Tecnologias</a>
* **Python** - Lógica principal do projeto.
* **Pandas** - Tratamento e Análise de dados.
* **Selenium** - Automação e Scraping.
* **SQLite** - Armazenamento local dos dados.
* **Streamlit** - Interface Web.

<br>

<!----------- ⭐ Funcionalidades ---------->
## <a id="funcionalidades">⭐ Funcionalidades</a>
* ✅ Coleta de dados de forma automatizada.
* ✅ Armazenamento em um Banco de Dados.
* ✅ Dashboard interativo com estatísticas e gráficos.
* ✅ Tabela dinãmica e estilizada com filtros relacionais.
* ✅ Opção de Baixar os arquivos em formato CSV.

<br>

<!----------- 📄 Funcionamento do Script de Extração ---------->
## <a id="funcionamento-do-script-de-extração">📄 Funcionamento do Script de Extração</a>
Abaixo contém um fluxograma mostrando de maneira simples como o scrpit de extração funciona.

<img width="700" height="700" alt="_Fluxograma" src="https://github.com/user-attachments/assets/553e48f3-985d-427b-ae88-b25c50fefea3" />

<br>

<!----------- ⚙️ Como Executar - Passo a Passo ---------->
## <a id="como-executar---passo-a-passo">⚙️ Como Executar - Passo a Passo</a>
> Requisitos: **Python 3.10+**

```bash
# 1) Clonar o repositório
git clone https://github.com/MathGeneze/Web-Scraping-Mercado-Livre.git
```
```bash
# 2) Instalar dependências
pip install -r requirements.txt
```
```bash
# 3) Executar o app
streamlit run navigation.py
```

<br>

<!----------- 🗂️ Estrutura do Projeto ---------->
## <a id="estrutura-do-projeto">🗂️ Estrutura do Projeto</a>
Abaixo contém a estrutura do projeto:

```bash
📦 Estrutura
 ┣ 📂 data                     # Dados e banco de dados local  
 ┃ ┗ 🗄️ banco.db
 ┃
 ┣ 📂 fonts                    # Arquivos de referência / documentação por tecnologia*
 ┣ 📂 pages                    # Páginas da aplicação Streamlit
 ┃ ┣ 🐍 main.py                # Página principal (Home)
 ┃ ┣ 🐍 visao_geral.py         # Visão geral dos dados
 ┃ ┗ 🐍 web_scraping.py        # Página explicando o scraping
 ┃
 ┣ 📂 src                      # Código-fonte principal
 ┃ ┣ 📂 extracao               # Módulo de extração de dados
 ┃ ┃ ┗ 🐍 extracao_dados.py
 ┃ ┃
 ┃ ┗ 📂 metricas               # Cálculo e análise de métricas
 ┃   ┗ 🐍 estatisticas.py
 ┃
 ┣ 📂 style                    # Estilos visuais da aplicação
 ┃ ┣ 📂 icons
 ┃ ┣ 📂 image
 ┃ ┣ 📂 videos
 ┃ ┣ 🎨 style.css
 ┃ ┣ 🎨 style2.css
 ┃ ┗ 🎨 style3.css
 ┃
 ┗ 📘 README.md
```

<br>

<!----------- 📸 Imagens do Projeto ---------->
## <a id="imagens-do-projeto">📸 Imagens do Projeto</a>
### 1️⃣ Home: Página inicial + Tabela com produtos
<img width="550" height="550" alt="image" src="https://github.com/user-attachments/assets/539f8365-79d7-47fe-a01e-6e21bc7c8407" />

### 2️⃣ Home: Fitros da Tabela
<img width="550" height="550" alt="image" src="https://github.com/user-attachments/assets/f8b0dd7b-6e7d-4f99-8d6c-fb28f0df4dcf" />

### 3️⃣ Home: Visualização única dos produtos extraídos
<img width="550" height="550" alt="image" src="https://github.com/user-attachments/assets/8b4bb47c-a77e-4c83-ba94-e22dca83682f" />

### 4️⃣ Home: Estatísticas dos produtos 
<img width="550" height="550" alt="image" src="https://github.com/user-attachments/assets/52ae2f7e-aaca-4cc3-9a70-8e44a3d116db" />

### 5️⃣ Home: Gráfico Dinâmico 
<img width="550" height="550" alt="image" src="https://github.com/user-attachments/assets/71a71fef-3cc0-4747-8340-3c1fc0a47d8c" />

### 6️⃣ Visão Geral: Explicação do projeto
<img width="550" height="550" alt="image" src="https://github.com/user-attachments/assets/a1ff3140-7e4d-4155-9e3c-e48d1fc41552" />

### 7️⃣ Extração de Dados: Explicação do script de extração
<img width="550" height="550" alt="image" src="https://github.com/user-attachments/assets/2e72932c-b8b2-4cf8-a0c8-8f7314a03d87" />

<br>

<!----------- 💡 Aprendizados ---------->
## <a id="aprendizados">💡 Aprendizados</a>
Este projeto foi extremamente relevante para mim. Além de aprender sobre extração de dados, ainda reforcei meus conhecimentos em SQL e salvei os dados em um banco de dados (no começo do projeto, eles eram salvos em arquivos csv). Também aprendi a importância de planejar a Estrutura de um Projeto, pois ao longo deste espeficadamente, as páginas do site foram surgindo ao longo do tempo sem planejamento. 



