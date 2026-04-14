# app/routes/chat.py
from flask import Blueprint, request, jsonify
from app.services.llm_service import get_assistant_response
from app.models.chat import ChatMessage
from app.extensions import db

bp = Blueprint('chat', __name__)

@bp.route('/', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message')
    session_id = data.get('session_id')

    # salva messaggio utente
    msg = ChatMessage(session_id=session_id, role='user', content=user_message)
    db.session.add(msg)
    db.session.commit()

    # chiama LLM (con RAG)
    response = get_assistant_response(user_message, session_id)

    # salva risposta assistente
    reply = ChatMessage(session_id=session_id, role='assistant', content=response)
    db.session.add(reply)
    db.session.commit()

    return jsonify({'reply': response})

@bp.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    messages = ChatMessage.query.filter_by(session_id=session_id).all()
    return jsonify([m.to_dict() for m in messages])