from urllib.parse import urlparse

from sqlalchemy import create_engine

from app.core.config import settings


parsed_url = urlparse(settings.database_url)

print("DATABASE CONFIG:")
print("Driver:", parsed_url.scheme)
print("Host:", parsed_url.hostname)
print("Port:", parsed_url.port)
print("Database:", parsed_url.path.lstrip("/"))


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)