from LERT.db.database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Administrator(Base):
    __tablename__ = 'Administrator'

    idAdmin = Column(Integer, primary_key=True)
    name = Column(String(100))
    #idUser = Column(Integer, ForeignKey('User.idUser'))
    #user = relationship("User", back_populates="admin")
