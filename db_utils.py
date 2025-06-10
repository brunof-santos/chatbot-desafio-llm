# Importando as bibliotecas necessárias
import boto3
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Carregando variáveis do .env
load_dotenv()
ATHENA_DATABASE = os.getenv("ATHENA_DATABASE_NAME")
ATHENA_OUTPUT = os.getenv("ATHENA_OUTPUT_LOCATION")

# Criando o client do boto3
athena_client = boto3.client(
    'athena',
    region_name='us-east-1',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

# Função responsável por executar a query no Athena e retornar um DataFrame
def executar_query(query: str) -> pd.DataFrame:
    # Iniciando a execução da query
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': ATHENA_DATABASE},
        ResultConfiguration={'OutputLocation': ATHENA_OUTPUT}
    )

    # Obtendo o ID da execução da query
    query_execution_id = response['QueryExecutionId']

    # Monitorando o status da execução (esperando até finalizar)
    while True:
        status_response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = status_response['QueryExecution']['Status']['State']

        # Imprimindo status no log (opcional para debug)
        print(f"Status da query: {status}")

        # Verificando se terminou com sucesso
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break

        # Aguardando um pouco antes de checar de novo
        time.sleep(1)

    # Tratando possíveis erros
    if status != 'SUCCEEDED':
        print(f"Erro ao executar query: {status}")
        return pd.DataFrame()  # Retornando df vazio em caso de falha

    # Recuperando o resultado da query
    result_response = athena_client.get_query_results(QueryExecutionId=query_execution_id)

    # Extraindo os nomes das colunas
    columns = [col['VarCharValue'] for col in result_response['ResultSet']['Rows'][0]['Data']]

    # Extraindo as linhas de dados (pulando a primeira linha que é o header)
    rows = []
    for row in result_response['ResultSet']['Rows'][1:]:
        rows.append([col.get('VarCharValue', None) for col in row['Data']])

    # Construindo o df
    df = pd.DataFrame(rows, columns=columns)

    # Retornando o df
    return df