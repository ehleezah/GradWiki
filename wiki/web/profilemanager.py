from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Apekshya/Desktop/Semester-4/Software Engineering/Project/wiki_flask/GradWiki/wiki/web/database.db'
db = SQLAlchemy()


with app.app_context():
    db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30))
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(10))
    address = db.Column(db.String(100))

    def __init__(self, fullname, username, password, email, phone, address):
        self.fullname = fullname
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.address = address

    def __repr__(self):
        return '<User {}>'.format(self.username)
