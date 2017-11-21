from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# load config
app.config.from_object('config')

# load database
db = SQLAlchemy(app)

# setup login/session manager
login_manager = LoginManager()
login_manager.init_app(app)


from app import views, models
