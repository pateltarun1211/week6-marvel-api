from flask import Flask
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from marvel_inventory.helpers import JSONEncoder
from marvel_inventory.models import db as root_db, login_manager, ma
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)

root_db.init_app(app)
migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin'

ma.init_app(app)
app.json_encoder = JSONEncoder

CORS(app)