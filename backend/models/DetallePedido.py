from sqlalchemy import Column, Integer, Float, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship

class DetallePedido(Base):
    __tablename__ = "detallepedido"
    id = Column(Integer, primary_key=True)
    pedidoid = Column(Integer, ForeignKey('pedido.id'))
    proteinaid = Column(Integer, ForeignKey('proteina.id'))
    tipalmuerzoid = Column(Integer, ForeignKey('tipoalmuerzo.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    total = Column(Float)

    #relaciones
    pedido= relationship("Pedido", back_populates= "detalle_pedido")
    proteina= relationship("Proteina", back_populates= "detalle_pedido")
    tipoalmuerzo= relationship("TipoAlmuerzo", back_populates= "detalle_pedido")