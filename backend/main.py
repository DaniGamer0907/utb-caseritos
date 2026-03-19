from fastapi import FastAPI
from models.base import Base
from db import engine

from routes.Cliente_routes import router as cliente_router
from routes.Proteina_routes import router as proteina_router
from routes.TipoAlmuerzo_routes import router as tipo_almuerzo_router
from routes.Almuerzo_routes import router as almuerzo_router
from routes.Pedido_routes import router as pedido_router
from routes.DetallePedido_routes import router as detalle_router
from routes.Pago_routes import router as pago_router

app = FastAPI(title="API Caseritos")


Base.metadata.create_all(bind=engine)


app.include_router(cliente_router)
app.include_router(proteina_router)
app.include_router(tipo_almuerzo_router)
app.include_router(almuerzo_router)
app.include_router(pedido_router)
app.include_router(detalle_router)
app.include_router(pago_router)

@app.get("/")
def root():
    return {"message": "API funcionando"}