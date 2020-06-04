# -*- coding: utf-8 -*-
# Python 3.7.7 required
import os

from flask import Flask

import auth_blueprint
import store_blueprint
from models import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(auth_blueprint.bp)
app.register_blueprint(store_blueprint.bp)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
