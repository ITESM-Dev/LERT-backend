from LERT.db.database import db
class Resource(db.Model):
    __tablename__ = 'Resource'
    
    idSerial = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(120))
    idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'))
    user = db.relationship("User", back_populates="resource")