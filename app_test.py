# app_test.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Circe2635!@localhost/zoovision'
app.secret_key = "flask rocks!"

db = SQLAlchemy(app)
