from aiohttp import web

from app.models.ship_order import ShipOrder

async def get_all_ship_orders(request):
    connection = request.app['db']
    orders = await ShipOrder.get_all(connection)
    return web.json_response([order.__dict__ for order in orders])

async def get_ship_order(request):
    connection = request.app['db']
    order_id = int(request.match_info['id'])
    order = await ShipOrder.get_by_id(connection, order_id)
    if order:
        return web.json_response(order.__dict__)
    raise web.HTTPNotFound(text='Ship order not found')

async def create_ship_order(request):
    connection = request.app['db']
    data = await request.json()
    client_id = data.get('client_id')
    ship_company_id = data.get('ship_company_id')
    if not client_id or not ship_company_id:
        raise web.HTTPBadRequest(text='Missing required fields')
    order = await ShipOrder.create(connection, client_id, ship_company_id)
    return web.json_response(order.__dict__, status=201)

async def update_ship_order(request):
    connection = request.app['db']
    order_id = int(request.match_info['id'])
    data = await request.json()
    client_id = data.get('client_id')
    ship_company_id = data.get('ship_company_id')
    if not client_id or not ship_company_id:
        raise web.HTTPBadRequest(text='Missing required fields')
    order = await ShipOrder.update(connection, order_id, client_id, ship_company_id)
    if order:
        return web.json_response(order.__dict__)
    raise web.HTTPNotFound(text='Ship order not found')

async def delete_ship_order(request):
    connection = request.app['db']
    order_id = int(request.match_info['id'])
    deleted = await ShipOrder.delete(connection, order_id)
    if deleted:
        return web.Response(text='Deleted', status=204)
    raise web.HTTPNotFound(text='Ship order not found')

def setup_ship_order_routes(app):
    app.router.add_get('/ship_orders', get_all_ship_orders)
    app.router.add_get('/ship_orders/{id}', get_ship_order)
    app.router.add_post('/ship_orders', create_ship_order)
    app.router.add_put('/ship_orders/{id}', update_ship_order)
    app.router.add_delete('/ship_orders/{id}', delete_ship_order)

