from aiohttp import web

from app.models.item import Item

async def get_all_items(request):
    connection = request.app['db']
    items = await Item.get_all(connection)
    return web.json_response([item.__dict__ for item in items])

async def get_item(request):
    connection = request.app['db']
    item_id = int(request.match_info['id'])
    item = await Item.get_by_id(connection, item_id)
    if item:
        return web.json_response(item.__dict__)
    raise web.HTTPNotFound(text='Item not found')

async def create_item(request):
    connection = request.app['db']
    data = await request.json()
    shipment_id = data.get('shipment_id')
    name = data.get('name')
    quantity = data.get('quantity')
    if not shipment_id or not name or quantity is None:
        raise web.HTTPBadRequest(text='Missing required fields')
    item = await Item.create(connection, shipment_id, name, quantity)
    return web.json_response(item.__dict__, status=201)

async def update_item(request):
    connection = request.app['db']
    item_id = int(request.match_info['id'])
    data = await request.json()
    shipment_id = data.get('shipment_id')
    name = data.get('name')
    quantity = data.get('quantity')
    if not shipment_id or not name or quantity is None:
        raise web.HTTPBadRequest(text='Missing required fields')
    item = await Item.update(connection, item_id, shipment_id, name, quantity)
    if item:
        return web.json_response(item.__dict__)
    raise web.HTTPNotFound(text='Item not found')

async def delete_item(request):
    connection = request.app['db']
    item_id = int(request.match_info['id'])
    deleted = await Item.delete(connection, item_id)
    if deleted:
        return web.Response(text='Deleted', status=204)
    raise web.HTTPNotFound(text='Item not found')


def setup_item_routes(app):
    app.router.add_get('/items', get_all_items)
    app.router.add_get('/items/{id}', get_item)
    app.router.add_post('/items', create_item)
    app.router.add_put('/items/{id}', update_item)
    app.router.add_delete('/items/{id}', delete_item)

