from LERT.db.database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__='User'

    idUser = Column(Integer, primary_key=True)
    name = Column(String(100))
    mail = Column(String(100), unique=True)
    password = Column(String(100))
    token = Column(String(100))
    expiration = Column(Integer)
    role = Column(String(100))
    admin = relationship("Administrator", back_populates="user", uselist=False)
    ica_admin = relationship("ICAAdmin", back_populates="user", uselist=False)
    opManager = relationship("OpManager", back_populates="user", uselist=False)
    manager = relationship("Manager", back_populates="user", uselist=False)
    resource = relationship("Resource", back_populates="user", uselist=False)
