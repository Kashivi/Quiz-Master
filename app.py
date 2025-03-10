from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from models.models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)