from LERT.db.database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
class Resource(Base):
    __tablename__ = 'Resource'
    
    idSerial = Column(Integer, primary_key=True)
    idUser = Column(Integer, ForeignKey('User.idUser'))
    user = relationship("User", back_populates="resource")