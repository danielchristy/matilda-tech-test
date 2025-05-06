'''
attempt at creating a custom migrations manager since i'm not using django
also trying to avoid using more tools like sqlalchemy/alembic (even if that would have been faster and easier..)
'''

import asyncpg

class MigrationManager:
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection

    async def create_migrations_log(self):
        try:
            await self.connection.execute(
                """
                    CREATE TABLE IF NOT EXISTS migration_log (
                        id SERIAL PRIMARY KEY,
                        filename TEXT UNIQUE NOT NULL,
                        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """
            )
        except Exception as err:
            print(f'error: {err}')
            raise

    async def migrations_applied(self, filename: str) -> bool:
        result = await self.connection.fetchval(
            "SELECT 1 FROM migration_log WHERE filename = $1", filename
        )
        return bool(result)
    
    async def log_migration(self, filename: str):
        try:
            await self.connection.execute(
                "INSERT INTO migration_log (filename) VALUES ($1)", filename
            )
        except Exception as err:
            print(f'error: {err}')
            raise