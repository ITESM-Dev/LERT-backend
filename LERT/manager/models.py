from LERT.db.database import db


class Manager(db.Model):
    idManager = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer)
    idOPManager = db.Column(db.Integer)
    idICA_Admin = db.Column(db.Integer)

#def __init__(self, name, email):
#    self.name = name
#    self.email = email
