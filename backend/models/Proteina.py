from sqlalchemy import Column, Integer, String
from models.base import Base
from sqlalchemy.orm import relationship


class Proteina(Base):
    __tablename__ = "proteina"
    id = Column(Integer,primary_key=True)
    nombre = Column(String)
    avaliable = Column(Integer)

    #relaciones
    detalle_pedido = relationship("DetallePedido", back_populates= "proteina")

