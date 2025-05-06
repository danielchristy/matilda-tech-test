from aiohttp import web

from app.models.shipping_company import ShippingCompany

async def get_all_shipping_companies(request):
    connection = request.app['db']
    shipping_company = await ShippingCompany.get_all(connection)
    return web.json_response([company.__dict__ for company in shipping_company])

async def get_shipping_company(request):
    connection = request.app['db']
    ship_company_id = int(request.match_info['id'])
    company = await ShippingCompany.get_by_id(connection, ship_company_id)
    if company:
        return web.json_response(company.__dict__)
    raise web.HTTPNotFound(text='Shipping company not found')

async def create_shipping_company(request):
    connection = request.app['db']
    data = await request.json()
    name = data.get('name')
    if not name:
        raise web.HTTPBadRequest(text='Missing name')
    company = await ShippingCompany.create(connection, name)
    return web.json_response(company.__dict__, status=201)

async def update_shipping_company(request):
    connection = request.app['db']
    ship_company_id = int(request.match_info['id'])
    data = await request.json()
    name = data.get('name')
    if not name:
        raise web.HTTPBadRequest(text='Missing name')
    company = await ShippingCompany.update(connection, ship_company_id, name)
    if company:
        return web.json_response(company.__dict__)
    raise web.HTTPNotFound(text='Shipping company not found')

async def delete_shipping_company(request):
    connection = request.app['db']
    ship_company_id = int(request.match_info['id'])
    deleted = await ShippingCompany.delete(connection, ship_company_id)
    if deleted:
        return web.Response(text='Deleted', status=204)
    raise web.HTTPNotFound(text='Shipping company not found')

def setup_shipping_company_routes(app):
    app.router.add_get('/shipping_companies', get_all_shipping_companies)
    app.router.add_get('/shipping_companies/{id}', get_shipping_company)
    app.router.add_post('/shipping_companies', create_shipping_company)
    app.router.add_put('/shipping_companies/{id}', update_shipping_company)
    app.router.add_delete('/shipping_companies/{id}', delete_shipping_company)

