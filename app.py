from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from models.database import db
import os

def create_app():
    app = Flask(__name__ , template_folder='templates')
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    return app

app = create_app()
from controllers.controllers import *


if __name__ == "__main__":
    app.run(debug=True)