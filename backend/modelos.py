from sqlalchemy import Column,Integer,String, Float
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

class Almuerzo(Base):
    __tablename__ = "tipoalmuerzo"
    id = Column(Integer,primary_key=True)
    nombre = Column(String)
    precio = Column(Float)

Base.metadata.create_all(engine)