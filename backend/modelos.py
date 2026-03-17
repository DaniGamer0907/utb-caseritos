from sqlalchemy import Column,Integer,String, Float,Boolean, ForeignKey,Date
from sqlalchemy.orm import declarative_base
from db import engine

Base = declarative_base()

class Proteina(Base):
    __tablename__ = "proteina"
    id = Column(Integer,primary_key=True)
    nombre = Column(String)
    avaliable = Column(Integer)

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer,primary_key=True)
    nombre = Column(String, index=True)
    lastname = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)

class TipoAlmuerzo(Base):
    __tablename__ = "tipoalmuerzo"
    id = Column(Integer,primary_key=True)
    nombre = Column(String)
    precio = Column(Float)

class Pedido(Base):
    __tablename__ = "pedido"
    id = Column(Integer,primary_key=True)
    fecha_creacion = Column(Date)
    estado = Column(Boolean)
    sugerencia = Column(String)
    cliente_id = Column(Integer,ForeignKey('cliente.id'))

class Almuerzo(Base):
    __tablename__ = "almuerzo"
    id = Column(Integer,primary_key=True)
    descripcion = Column(String)
    fecha = Column(Date)
    proteinaid = Column(Integer, ForeignKey('proteina.id'))
    tipalmuerzo = Column(Integer,ForeignKey('tipoalmuerzo.id'))

class DetallePedidos(Base):
    __tablename__ = "detallepedido"
    id = Column(Integer, primary_key=True)
    pedidoid = Column(Integer, ForeignKey('pedido.id'))
    almuerzoid = Column(Integer, ForeignKey('almuerzo.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    total = Column(Float)

class pago(Base):
    __tablename__ = "pago"
    id = Column(Integer,primary_key=True)
    pedidoid = Column(Integer, ForeignKey('pedido.id'))
    metodopago = Column(String)
    diadelpago = Column(Date)
    monto = Column(Float)
    
Base.metadata.create_all(engine)