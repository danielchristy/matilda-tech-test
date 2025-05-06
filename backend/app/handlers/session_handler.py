from aiohttp import web
from app.models.session import get_session, cleanup_expired_sessions

@web.middleware
async def session_middleware(request, handler):
    # login, register, logout should be ignored?
    if request.path in ['/login', '/register', '/logout']:
        return await handler(request)
    
    cleanup_expired_sessions()
    
    session_id = request.cookies.get('session_id')
    if not session_id:
        raise web.HTTPUnauthorized(text='No active session')
    
    session = get_session(session_id)
    if not session:
        raise web.HTTPUnauthorized(text='Invalid or expired session')
    
    request['employee_id'] = session.employee_id
    
    return await handler(request) 