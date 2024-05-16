import os

from dotenv import load_dotenv

load_dotenv()

PSQL_CONNECTION_STRING = os.getenv("PSQL_CONNECTION_STRING")
