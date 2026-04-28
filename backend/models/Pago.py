from sqlalchemy import Column, Integer, Float, ForeignKey, String, Date
from models.base import Base
from sqlalchemy.orm import relationship

class Pago(Base):
    __tablename__ = "pago"
    id = Column(Integer,primary_key=True)
    metodopago = Column(String)
    diadelpago = Column(Date)
    monto = Column(Float)
    referencia = Column(String, nullable=True)

    #relaciones
    pedido = relationship("Pedido", back_populates="pago")