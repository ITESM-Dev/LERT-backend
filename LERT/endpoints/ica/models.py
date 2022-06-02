from LERT.db.database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class ICA(Base):
    __tablename__ = "ICA"

    idICA = Column(Integer, primary_key=True)
    icaCode = Column(String(120))
    icaCore = Column(String(120))
    year = Column(String(120))
    idPlanning = Column(String(50))
    icaOwner = Column(String(150))
    budget = Column(Float)
    country = Column(String(120))
    status = Column(String(200))
    depto = Column(String(50))
    frequencyBill = Column(String(50))
    cc = Column(String(50))
    ctyNameReq = Column(String(100))
    rCtyReq = Column(String(50))
    division = Column(String(50))
    major = Column(String(50))
    minor = Column(String(50))
    leru = Column(String(50))
    description = Column(String(200))
    type = Column(String(100))
    nec = Column(Integer)
    totalPlusTaxes = Column(Float)
    startDate = Column(Date)
    endDate = Column(Date)
    ctyNamePerf = Column(String(100))
    rCtyPerf = Column(String(50))
    totalBilling = Column(Float)
    manager = relationship("Manager", back_populates="ica")

