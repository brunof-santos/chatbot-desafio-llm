# Importando as bibliotecas necessárias
import openai
import os
from dotenv import load_dotenv

# Carregando as variáveis do arquivo .env
load_dotenv()

# Definindo a chave da OpenAI vinda do .env
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função responsável por gerar uma query SQL com base na pergunta natural escrita
def gerar_query_sql(pergunta: str) -> str:
    # Prompt padrão para o modelo da OpenAI
    prompt = f"""
    Gere uma consulta SQL no Athena com base na pergunta:
    "{pergunta}"

    A tabela se chama 'credito_data' e está no banco 'credito_database' e tem colunas:
    Considere que seu chatbot apenas precisa conhecer estas colunas (considere que nenhuma query irá utilizar informações de outras colunas):

    REF_DATE: data de referência do registro
    TARGET: alvo binário de inadimplência (1: Mau Pagador, i.e. atraso > 60 dias em 2 meses)
    VAR2: sexo (M ou F)
    IDADE: idade do indivíduo (número real)
    VAR4: flag de óbito (S se o indivíduo faleceu e vazia caso esteja vivo)
    VAR5: unidade federativa (UF) brasileira
    VAR8: classe social estimada

    Retorne apenas o código SQL por favor, seja objetivo.
    """

    # Chamando a API da OpenAI usando o modelo de chat
    resposta = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente que escreve consultas SQL para o Amazon AWS Athena."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    # Retornando apenas o conteúdo da resposta
    return resposta.choices[0].message.content.strip()