from sqlalchemy import Column,String,Integer
from models.base import Base
from sqlalchemy.orm import relationship

class Rol(Base):
    __tablename__ = "rol"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)

    #Relacion con Usuario
    usuario= relationship("Usuario", back_populates= "rol")
