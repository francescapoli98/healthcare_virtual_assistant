from flask import Flask
from .extensions import db, migrate, cors
from .routes import chat, appointments, patients, doctors

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    app.register_blueprint(chat.bp, url_prefix='/api/chat')
    app.register_blueprint(appointments.bp, url_prefix='/api/appointments')
    app.register_blueprint(patients.bp, url_prefix='/api/patients')
    app.register_blueprint(doctors.bp, url_prefix='/api/doctors')

    return app