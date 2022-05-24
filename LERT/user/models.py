from LERT.db.database import db
class User(db.Model):
    __tablename__='User'

    idUser = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mail = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    token = db.Column(db.String(100))
    expiration = db.Column(db.Integer)
    role = db.Column(db.String(100))
    admin = db.relationship("Administrator", back_populates="user", uselist=False)
    ica_admin = db.relationship("ICAAdmin", back_populates="user", uselist=False)
    opManager = db.relationship("OpManager", back_populates="user", uselist=False)
    manager = db.relationship("Manager", back_populates="user", uselist=False)
    resource = db.relationship("Resource", back_populates="user", uselist=False)
