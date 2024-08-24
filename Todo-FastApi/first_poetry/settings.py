from starlette.config import Config # type: ignore
from starlette.datastructures import Secret # type: ignore

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

myDatabase_url = config("Database_url", cast=Secret)

myTestDatabase_url = config("test_Database_url", cast=Secret)