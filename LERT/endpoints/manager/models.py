from LERT.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

association_table_Manager_Resource = Table(
    'manager_resource', Base.metadata,
    Column('idSerial', Integer, ForeignKey('Resource.idSerial')),
    Column('idManager', Integer, ForeignKey('Manager.idManager'))
)

class Manager(Base):
    __tablename__ = "Manager"

    idManager = Column(Integer, primary_key=True)
    idUser = Column(Integer, ForeignKey('User.idUser'))
    idOPManager = Column(Integer, ForeignKey('OpManager.idOPManager'))
    idICA_Admin = Column(Integer, ForeignKey('ICAAdmin.idICA_Admin'))
    idICA = Column(Integer, ForeignKey('ICA.idICA'))
    recoveryStatus = Column(String(30))
    status = Column(String(30))
    lastUpdated = Column(Date)
    tokenAuthenticator = Column(String(100))
    user = relationship("User", back_populates="manager")
    ica = relationship("ICA", back_populates="manager")
    resource = relationship("Resource", secondary=association_table_Manager_Resource)
    expense = relationship("Expense")
    