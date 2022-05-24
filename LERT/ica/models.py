from LERT.db.database import db


class ICA(db.Model):
    __tablename__ = "ICA"

    idICA = db.Column(db.Integer, primary_key=True)
    icaCode = db.Column(db.String(120))
    icaCore = db.Column(db.String(120))
    year = db.Column(db.String(120))
    idPlanning = db.Column(db.String(50))
    icaOwner = db.Column(db.String(150))
    budget = db.Column(db.Float)
    country = db.Column(db.String(120))
    status = db.Column(db.String(200))
    depto = db.Column(db.String(50))
    frequencyBill = db.Column(db.String(50))
    cc = db.Column(db.String(50))
    ctyNameReq = db.Column(db.String(100))
    rCtyReq = db.Column(db.String(50))
    division = db.Column(db.String(50))
    major = db.Column(db.String(50))
    minor = db.Column(db.String(50))
    leru = db.Column(db.String(50))
    description = db.Column(db.String(200))
    type = db.Column(db.String(100))
    nec = db.Column(db.Integer)
    totalPlusTaxes = db.Column(db.Float)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    ctyNamePerf = db.Column(db.String(100))
    rCtyPerf = db.Column(db.String(50))
    totalBilling = db.Column(db.Float)

