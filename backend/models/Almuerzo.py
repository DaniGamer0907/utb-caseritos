from sqlalchemy import Column, Integer, String, Date, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship

class Almuerzo(Base):
    __tablename__ = "almuerzo"
    id = Column(Integer,primary_key=True)
    fecha = Column(Date)
    proteinaid = Column(Integer, ForeignKey('proteina.id'))
    tipalmuerzo = Column(Integer,ForeignKey('tipoalmuerzo.id'))

    #relaciones
    tipo_almuerzo= relationship("TipoAlmuerzo", back_populates= "almuerzo")
    proteina= relationship("Proteina", back_populates= "almuerzo")
    detalle_pedido= relationship("DetallePedido", back_populates= "almuerzo")

