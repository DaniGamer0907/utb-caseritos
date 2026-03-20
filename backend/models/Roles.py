from sqlalchemy import Column,String
from models.base import Base
from sqlalchemy.orm import relationship

class Roles(Base):
    __tablename__ = "roles"
    nombre = Column(String)

    #Relacion con Usuario
    usuario= relationship("Usuario", back_populates= "roles")
