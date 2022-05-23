from LERT.db.database import db


class User(db.Model):
    idUser = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mail = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    token = db.Column(db.String(100))
    expiration = db.Column(db.Integer)
    role = db.Column(db.String(100))

def __init__(self, name, email):
    self.name = name
    self.email = email
