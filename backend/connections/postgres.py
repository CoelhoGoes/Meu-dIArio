import psycopg
from dotenv import load_dotenv
import os
load_dotenv()

from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()

class PostgresConnection:
    def __init__(self):
        # Lê as variáveis de ambiente
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = int(os.getenv("DB_PORT", 5432))  # padrão 5432

    def get_connection(self):
        """Cria e retorna uma nova conexão"""
        return psycopg.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port,
            sslmode="require"  
        )
