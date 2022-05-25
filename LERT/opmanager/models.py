from LERT.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *


class OpManager(Base):
    __tablename__ = 'OpManager'

    idOPManager = Column(Integer, primary_key=True)
    idUser = Column(Integer, ForeignKey('User.idUser'))
    status = Column(String(120))

    user = relationship("User", back_populates="opManager")
    manager = relationship("Manager")

    