from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    users = relationship("User", back_populates="role")
