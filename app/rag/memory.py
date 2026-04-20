SESSION_MEMORY = {}

def get_memory(session_id: int):
    return SESSION_MEMORY.get(session_id, [])

def add_message(session_id: int, role: str, message: str):
    SESSION_MEMORY.setdefault(session_id, []).append({
        "role": role,
        "content": message
    })

def get_recent_context(session_id: int, max_turns: int = 6):
    history = SESSION_MEMORY.get(session_id, [])
    return history[-max_turns:]
