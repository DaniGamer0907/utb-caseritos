from sqlalchemy import Column, Integer, String, Float
from models.base import Base
from sqlalchemy.orm import relationship

class TipoAlmuerzo(Base):
    __tablename__ = "tipoalmuerzo"
    id = Column(Integer,primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    precio = Column(Float)

    #relaciones
    almuerzo= relationship("Almuerzo", back_populates= "tipo_almuerzo")
    