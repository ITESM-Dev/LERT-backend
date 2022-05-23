from LERT.db.database import db
from LERT.user.models import User


class Resource(db.Model):
    idSerial = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(120))
    idUser = db.Column(db.Integer, db.ForeignKey(User.idUser))
    resource = db.relationship(User, uselist=False)