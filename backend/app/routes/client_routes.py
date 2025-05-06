from aiohttp import web

from app.models.client import Client

async def get_all_clients(request):
    connection = request.app['db']
    clients = await Client.get_all(connection)
    return web.json_response([client.__dict__ for client in clients])

async def get_client(request):
    connection = request.app['db']
    client_id = int(request.match_info['id'])
    client = await Client.get_by_id(connection, client_id)
    if client:
        return web.json_response(client.__dict__)
    raise web.HTTPNotFound(text='Client not found')

async def create_client(request):
    connection = request.app['db']
    data = await request.json()
    name = data.get('name')
    if not name:
        raise web.HTTPBadRequest(text='Missing name')
    client = await Client.create(connection, name)
    return web.json_response(client.__dict__, status=201)

async def update_client(request):
    connection = request.app['db']
    client_id = int(request.match_info['id'])
    data = await request.json()
    name = data.get('name')
    if not name:
        raise web.HTTPBadRequest(text='Missing name')
    client = await Client.update(connection, client_id, name)
    if client:
        return web.json_response(client.__dict__)
    raise web.HTTPNotFound(text='Client not found')

async def delete_client(request):
    connection = request.app['db']
    client_id = int(request.match_info['id'])
    deleted = await Client.delete(connection, client_id)
    if deleted:
        return web.Response(text='Deleted', status=204)
    raise web.HTTPNotFound(text='Client not found')

def setup_client_routes(app):
    app.router.add_get('/clients', get_all_clients)
    app.router.add_get('/clients/{id}', get_client)
    app.router.add_post('/clients', create_client)
    app.router.add_put('/clients/{id}', update_client)
    app.router.add_delete('/clients/{id}', delete_client)