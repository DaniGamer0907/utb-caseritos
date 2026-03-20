from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship

class Pedido(Base):
    __tablename__ = "pedido"
    id = Column(Integer,primary_key=True)
    fecha_creacion = Column(Date)
    estado = Column(Boolean)
    sugerencia = Column(String)
    usuario_id = Column(Integer,ForeignKey('usuario.id'))

    #relaciones
    usuario = relationship("Usuario", back_populates= "pedido")
    pago = relationship("Pago", back_populates= "pedido")
    detalle_pedido = relationship("DetallePedido", back_populates= "pedido")
