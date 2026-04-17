from flask import Flask
from .core import db
from .routes.chat import chat_bp
from .routes.appuntamenti import appuntamenti_bp
from .extensions import init_llm

def create_app():
    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    db.init_app(app)
    init_llm(app)
    ### servizi disponibili nell'app, ognuna salvata come un blueprint per modularità
    app.register_blueprint(chat_bp)
    app.register_blueprint(appuntamenti_bp)
    print(app.config["GOOGLE_API_KEY"]) ## DEBUG

    @app.route("/")
    def home():
        return {"message": "Backend attivo"}

    return app
