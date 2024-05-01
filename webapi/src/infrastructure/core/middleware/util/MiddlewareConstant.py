import os
from dotenv import load_dotenv

load_dotenv()

WEBAPI_AUTH_URL: str = os.getenv('WEBAPI_AUTH_URL', '')