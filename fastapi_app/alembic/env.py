from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context
from my_app.database import SQLALCHEMY_DATABASE_URL  # Adjust as needed

# Use synchronous engine instead of AsyncEngine
connectable = create_engine(SQLALCHEMY_DATABASE_URL)

def run_migrations_online():
    with connectable.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
