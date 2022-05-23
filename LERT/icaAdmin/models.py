from LERT.db.database import db
from LERT.user.models import User


class ICAAdmin(db.Model):
    idICA_Admin = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey(User.idUser))
    icaAdmin = db.relationship(User, uselist=False)

