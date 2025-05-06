import os
import asyncio
import asyncpg

from ..config import DATABASE_URL
from .migration_manager import MigrationManager

async def get_db_connection():
    try:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in your environment or config.")
        return await asyncpg.connect(DATABASE_URL)
    except Exception as e:
        print(f"[ERROR] Failed to connect to DB: {e}")
        return None

async def close_db_connection(connection):
    await connection.close()

async def run_db_migrations(connection):
    migration_manager = MigrationManager(connection)
    await migration_manager.create_migrations_log()

    current_dir = os.path.dirname(__file__)
    sql_scripts_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'migrations'))
    sql_scripts = sorted(script for script in os.listdir(sql_scripts_path) if script.endswith('.sql'))

    for filename in sql_scripts:
        if await migration_manager.migrations_applied(filename):
            print(f'migrations already applied to: {filename}')
            continue
        
        print(f'running migrations: {filename}')
        scriptpath = os.path.join(sql_scripts_path, filename)
        with open(scriptpath, 'r') as openfile:
            sql = openfile.read()
            try:
                await connection.execute(sql)
                await migration_manager.log_migration(filename)
                print(f'migrations applied to: {filename}')
            except Exception as err:
                print(f'migrations failed for: {filename} (error: {err})')
                raise


async def main():
    connection = await get_db_connection()
    try:
        await run_db_migrations(connection)
    finally:
        await close_db_connection(connection)

if __name__ == '__main__':
    asyncio.run(main())

