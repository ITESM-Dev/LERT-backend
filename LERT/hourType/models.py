from LERT.db.database import db


class HourType(db.Model):
    __tablename__ = "HourType"

    idHourType = db.Column(db.Integer, primary_key=True)
    idBandType = db.Column(db.Integer)
    type = db.Column(db.String(200))
    band = db.Column(db.String(50))
    country = db.Column(db.String(120))
    rate = db.Column(db.Float)
    dateToStart = db.Column(db.String(100))
    dateToFinish = db.Column(db.String(100))

    resourceExpense = db.relationship("ResourceExpense", back_populates="hourType", uselist=False)
