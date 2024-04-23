import os
from dotenv import load_dotenv

load_dotenv()

PSQL_USER: str = os.environ.get("POSTGRES_USER", 'postgres')
PSQL_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", 'postgres')
PSQL_HOST: str = os.environ.get("POSTGRES_HOST", 'postgres')
PSQL_PORT: int = int(os.environ.get("POSTGRES_PORT", 5432))
PSQL_DB: str = os.environ.get("POSTGRES_DB", 'postgres')