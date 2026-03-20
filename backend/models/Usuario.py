from sqlalchemy import Column, Integer, String
from models.base import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer,primary_key=True)
    nombre = Column(String, index=True)
    lastname = Column(String)
    password = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)

    #relaciones
    pedido= relationship("Pedido", back_populates= "usuario")

