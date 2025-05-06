import asyncio
from aiohttp import web
import aiohttp_cors
from aiohttp_cors import ResourceOptions

from app.handlers.database_handler import get_db_connection, close_db_connection, run_db_migrations
from app.handlers.session_handler import session_middleware

from app.routes.employee_routes import setup_employee_auth_routes
from app.routes.shipping_company_routes import setup_shipping_company_routes
from app.routes.client_routes import setup_client_routes
from app.routes.ship_order_routes import setup_ship_order_routes
from app.routes.shipment_routes import setup_shipment_routes
from app.routes.item_routes import setup_item_routes

async def start_app():
    app = web.Application(middlewares=[session_middleware])

    async def startup(app):
        try:
            connection = await get_db_connection()
            if connection is None:
                raise RuntimeError("Failed to establish a database connection.")

            app['db'] = connection
            await run_db_migrations(app['db'])

            setup_employee_auth_routes(app)
            setup_shipping_company_routes(app)
            setup_client_routes(app)
            setup_ship_order_routes(app)
            setup_shipment_routes(app)
            setup_item_routes(app)

            cors = aiohttp_cors.setup(app)
            for route in list(app.router.routes()):
                cors.add(route, {
                    "http://localhost:3000": ResourceOptions(
                        allow_credentials=True,
                        expose_headers="*",
                        allow_headers="*",
                    )
                })
        except Exception as err:
            print(f'Database startup failed: {err}')
            raise

    app.on_startup.append(startup)

    async def cleanup(app):
        if 'db' in app:
            await close_db_connection(app['db'])

    app.on_cleanup.append(cleanup)

    return app

if __name__ == '__main__':
    app = asyncio.run(start_app())
    web.run_app(app, host='127.0.0.1', port=8080)