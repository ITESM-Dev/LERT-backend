from LERT.db.database import db


class OpManager(db.Model):
    idOPManager = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer)
    status = db.Column(db.String(120))

#def __init__(self, name, email):
#    self.name = name
#    self.email = email
