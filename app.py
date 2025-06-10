# Importando as bibliotecas necessárias
import streamlit as st
from llm_utils import gerar_query_sql
from db_utils import executar_query
from viz_utils import gerar_grafico

# Configurações da página
st.set_page_config(page_title="💬 Chatbot de Crédito", layout="wide")
st.title("Chatbot de Crédito 🤖")

# Caixa de input da pergunta
pergunta = st.text_input("Digite sua pergunta sobre os dados: ")

# Check se tem algo
if pergunta:
    # Mostrando spinner de carregamento enquanto processa
    with st.spinner("Consultando GPT e gerando resultados..."):

        # Criação da query
        query = gerar_query_sql(pergunta)
        st.code(query, language="sql")

        # Execução da query
        df = executar_query(query)

        # Mostrando o df
        st.write(df)

        # Geração do gráfico
        grafico = gerar_grafico(df)
        if grafico:
            st.plotly_chart(grafico, use_container_width=True)
