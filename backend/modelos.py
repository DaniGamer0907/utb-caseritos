from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base
from db import engine

Base = declarative_base()

class Proteina(Base):
    __tablename__ = "proteina"
    Protein_id = Column(Integer,primary_key=True)
    nombre = Column(String)
    avaliable = Column(Integer)

Base.metadata.create_all(engine)