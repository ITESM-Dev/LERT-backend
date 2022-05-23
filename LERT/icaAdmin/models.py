from LERT.db.database import db

class ICAAdmin(db.Model):
    __tablename__='ICAAdmin'

    idICA_Admin = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'))
    user = db.relationship("User", back_populates="ica_admin")
