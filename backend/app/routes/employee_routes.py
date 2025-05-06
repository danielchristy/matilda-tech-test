from aiohttp import web
from app.models.employee import Employee
from app.models.session import create_session, delete_session

async def register(request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise web.HTTPBadRequest(text="Username and password required")

    connection = request.app['db']
    existing_user = await Employee.get_by_username(connection, username)
    if existing_user:
        raise web.HTTPConflict(text="Employee already exists")

    employee = await Employee.create(connection, username, password)
    return web.json_response({"employee_id": employee.employee_id, "username": employee.username}, status=201)


async def login(request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise web.HTTPBadRequest(text="Username and password required")

    connection = request.app['db']
    employee = await Employee.get_by_username(connection, username)
    if not employee or not employee.check_password(password):
        raise web.HTTPUnauthorized(text="Invalid credentials")

    session_id = create_session(employee.employee_id)
    
    response = web.json_response({"message": "Login successful"})
    response.set_cookie("session_id", session_id, max_age=86400, httponly=True, secure=False, samesite='Lax')
    return response


async def logout(request):
    session_id = request.cookies.get("session_id")
    if session_id:
        delete_session(session_id)
    response = web.Response(text="Logged out")
    response.del_cookie("session_id")
    return response


def setup_employee_auth_routes(app):
    app.router.add_post('/register', register)
    app.router.add_post('/login', login)
    app.router.add_post('/logout', logout)
