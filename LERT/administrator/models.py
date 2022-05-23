from LERT.db.database import db
from LERT.user.models import User


class Administrator(db.Model):
    idAdmin = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey(User.idUser))
    admin = db.relationship(User, uselist=False)

