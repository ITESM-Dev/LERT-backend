from LERT.db.database import Base
from LERT.user.models import User
from sqlalchemy import *
from sqlalchemy.orm import relationship

class ICAAdmin(Base):
    __tablename__='ICAAdmin'

    idICA_Admin = Column(Integer, primary_key=True)
    idUser = Column(Integer, ForeignKey(User.idUser))
    user = relationship("User", back_populates="ica_admin")
    manager = relationship("Manager")
