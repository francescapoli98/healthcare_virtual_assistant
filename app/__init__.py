from flask import Flask
from flask_cors import CORS
from .core import db
from .routes.chat import chat_bp
from .routes.appuntamenti import appuntamenti_bp
from .extensions import create_llm

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173"])

    app.config.from_object("app.config.Config")

    db.init_app(app)
    app.llm = create_llm(app)
    ### servizi disponibili nell'app, ognuna salvata come un blueprint per modularità
    app.register_blueprint(chat_bp)
    app.register_blueprint(appuntamenti_bp)

    @app.route("/")
    def home():
        return {"message": "Backend attivo"}

    return app
