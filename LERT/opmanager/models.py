from LERT.db.database import db


class OpManager(db.Model):
    __tablename__ = 'OpManager'

    idOPManager = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'))
    status = db.Column(db.String(120))

    user = db.relationship("User", back_populates="opManager")

    