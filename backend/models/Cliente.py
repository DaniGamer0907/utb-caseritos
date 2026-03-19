from sqlalchemy import Column, Integer, String
from models.base import Base
from sqlalchemy.orm import relationship

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer,primary_key=True)
    nombre = Column(String, index=True)
    lastname = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)

    #relaciones
    pedido= relationship("Pedido", back_populates= "cliente")

