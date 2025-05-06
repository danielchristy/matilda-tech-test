import time
from typing import Dict, Optional
import bcrypt

class Session:
    def __init__(self, employee_id: int, created_at: float, expires_at: float):
        self.employee_id = employee_id
        self.created_at = created_at
        self.expires_at = expires_at

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

SESSIONS: Dict[str, Session] = {}

def create_session_id(employee_id: int) -> str:
    salt = bcrypt.gensalt().decode()
    return f"session:{employee_id}:{salt}"

def create_session(employee_id: int, session_duration: int = 86400) -> str:
    for session_id, session in list(SESSIONS.items()):
        if session.employee_id == employee_id:
            del SESSIONS[session_id]
    
    session_id = create_session_id(employee_id)
    now = time.time()
    SESSIONS[session_id] = Session(
        employee_id=employee_id,
        created_at=now,
        expires_at=now + session_duration
    )
    return session_id

def get_session(session_id: str) -> Optional[Session]:
    session = SESSIONS.get(session_id)
    if session and not session.is_expired:
        return session
    if session:
        del SESSIONS[session_id]
    return None

def delete_session(session_id: str) -> None:
    if session_id in SESSIONS:
        del SESSIONS[session_id]

def cleanup_expired_sessions() -> None:
    for session_id, session in list(SESSIONS.items()):
        if session.is_expired:
            del SESSIONS[session_id] 