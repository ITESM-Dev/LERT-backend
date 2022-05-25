from LERT.db.database import db


class BandType(db.Model):
    __tablename__ = "BandType"

    idBandType = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200))
    band = db.Column(db.String(50))
    country = db.Column(db.String(120))
    yearlyRate = db.Column(db.Float) 
    dateToStart = db.Column(db.String(100))

    hourType = db.relationship("HourType", back_populates="bandType", uselist=False)