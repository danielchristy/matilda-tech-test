from aiohttp import web

from app.models.shipment import Shipment

async def get_all_shipments(request):
    connection = request.app['db']
    shipments = await Shipment.get_all(connection)
    return web.json_response([shipment.__dict__ for shipment in shipments])

async def get_shipment(request):
    connection = request.app['db']
    shipment_id = int(request.match_info['id'])
    shipment = await Shipment.get_by_id(connection, shipment_id)
    if shipment:
        return web.json_response(shipment.__dict__)
    raise web.HTTPNotFound(text='Shipment not found')

async def create_shipment(request):
    connection = request.app['db']
    data = await request.json()
    ship_order_id = data.get('ship_order_id')
    shipment_state = data.get('shipment_state')
    if not ship_order_id or not shipment_state:
        raise web.HTTPBadRequest(text='Missing required fields')
    shipment = await Shipment.create(connection, ship_order_id, shipment_state)
    return web.json_response(shipment.__dict__, status=201)

async def update_shipment(request):
    connection = request.app['db']
    shipment_id = int(request.match_info['id'])
    data = await request.json()
    ship_order_id = data.get('ship_order_id')
    shipment_state = data.get('shipment_state')
    if not ship_order_id or not shipment_state:
        raise web.HTTPBadRequest(text='Missing required fields')
    shipment = await Shipment.update(connection, shipment_id, ship_order_id, shipment_state)
    if shipment:
        return web.json_response(shipment.__dict__)
    raise web.HTTPNotFound(text='Shipment not found')

async def delete_shipment(request):
    connection = request.app['db']
    shipment_id = int(request.match_info['id'])
    deleted = await Shipment.delete(connection, shipment_id)
    if deleted:
        return web.Response(text='Deleted', status=204)
    raise web.HTTPNotFound(text='Shipment not found')

def setup_shipment_routes(app):
    app.router.add_get('/shipments', get_all_shipments)
    app.router.add_get('/shipments/{id}', get_shipment)
    app.router.add_post('/shipments', create_shipment)
    app.router.add_put('/shipments/{id}', update_shipment)
    app.router.add_delete('/shipments/{id}', delete_shipment)

