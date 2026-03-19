from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="2006",
    host="localhost",
    database="Caseritos",
    port=5432
)

engine = create_engine(url)
SessionLocal = sessionmaker(bind= engine, autocommit = False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
        print("Conexion lista")
    finally:
        db.close()