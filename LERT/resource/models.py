from LERT.db.database import Base
from LERT.user.models import User
from sqlalchemy import *
from sqlalchemy.orm import relationship
class Resource(Base):
    __tablename__ = 'Resource'
    
    idSerial = Column(Integer, primary_key=True)
    country = Column(String(120))
    idUser = Column(Integer, ForeignKey(User.idUser))
    user = relationship("User", back_populates="resource")