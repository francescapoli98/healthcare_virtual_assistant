from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
# cors = CORS(resources={r"/api/*": {"origins": "http://localhost:3000"}})
