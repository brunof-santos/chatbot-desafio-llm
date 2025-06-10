# Importando as bibliotecas necessárias
import plotly.express as px
import pandas as pd

# Criando função para gerar gráficos
def gerar_grafico(df: pd.DataFrame):
    # Verificando se há duas colunas no df (x e y)
    if df.shape[1] == 2:
        x, y = df.columns

        # Criando um gráfico de barras simples com plotly
        return px.bar(df, x=x, y=y, title="Gráfico gerado pela consulta")

    # Se o df não tiver o formato esperado, retorna None
    return None