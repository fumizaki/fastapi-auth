import os
from dotenv import load_dotenv

load_dotenv()

OAUTH2_ISSUER: str = os.environ.get("OAUTH2_ISSUER", '')
OAUTH2_AUDIENCE: str = os.environ.get("OAUTH2_AUDIENCE", '')
OAUTH2_TOKEN_ALGORITHM: str = os.getenv('OAUTH2_TOKEN_ALGORITHM', '')
OAUTH2_TOKEN_SECRET: str = os.getenv('OAUTH2_TOKEN_SECRET', '')
OAUTH2_TOKEN_REFRESH_ALGORITHM: str = os.getenv('OAUTH2_TOKEN_REFRESH_ALGORITHM', '')
OAUTH2_TOKEN_REFRESH_SECRET: str = os.getenv('OAUTH2_TOKEN_REFRESH_SECRET', '')