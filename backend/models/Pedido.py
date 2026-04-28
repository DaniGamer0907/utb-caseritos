from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Pedido(Base):
    __tablename__ = "pedido"
    id = Column(Integer,primary_key=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow())
    estado = Column(String) # nequi, efectivo, confirmado, entregado, cancelado
    sugerencia = Column(String)
    total = Column(Float)
    usuario_id = Column(Integer,ForeignKey('usuario.id'))
    pago_id = Column(Integer, ForeignKey('pago.id'))

    #relaciones
    usuario = relationship("Usuario", back_populates= "pedido")
    pago = relationship("Pago", back_populates= "pedido")
    detalle_pedido = relationship("DetallePedido", back_populates= "pedido")
