from LERT.db.database import Base
from sqlalchemy.orm import relationship
from LERT.user.models import User
from LERT.opmanager.models import OpManager
from LERT.icaAdmin.models import ICAAdmin
from sqlalchemy import *

class Manager(Base):
    __tablename__ = "Manager"

    idManager = Column(Integer, primary_key=True)
    idUser = Column(Integer, ForeignKey(User.idUser))
    idOPManager = Column(Integer, ForeignKey(OpManager.idOPManager))
    idICA_Admin = Column(Integer, ForeignKey(ICAAdmin.idICA_Admin))

    user = relationship("User", back_populates="manager")
    expense = relationship("Expense")
    