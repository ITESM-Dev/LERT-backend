from LERT.db.database import db

class Administrator(db.Model):
    __tablename__='Administrator'
    idAdmin = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'))
    user = db.relationship("User", back_populates="admin")
