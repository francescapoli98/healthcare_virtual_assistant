from flask import Flask
from flask_cors import CORS
from .core import db
from .routes.chat import chat_bp
from .routes.appuntamenti import appuntamenti_bp
from .routes.authentication import auth_bp
from .extensions import get_llm
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = "cambia_questa_chiave_in_produzione"
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    app.config.from_object("app.config.Config")

    db.init_app(app)
    app.llm = None#create_llm(app)
    ### servizi disponibili nell'app, ognuna salvata come un blueprint per modularità
    app.register_blueprint(chat_bp)
    app.register_blueprint(appuntamenti_bp, url_prefix="/appuntamenti")
    app.register_blueprint(auth_bp)
    @app.route("/")
    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        traceback.print_exc()
        return {"error": str(e)}, 500
   
    def home():
        return {"message": "Backend attivo"}

    return app
