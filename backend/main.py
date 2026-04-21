from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.base import Base
from db import engine

from models.Rol import Rol
from routes.auth import router as auth_router
from routes.Usuario_routes import router as usuario_router
from routes.Proteina_routes import router as proteina_router
from routes.TipoAlmuerzo_routes import router as tipo_almuerzo_router
from routes.Almuerzo_routes import router as almuerzo_router
from routes.Pedido_routes import router as pedido_router
from routes.DetallePedido_routes import router as detalle_router
from routes.Pago_routes import router as pago_router

app = FastAPI(title="API Caseritos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], # El puerto de Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(proteina_router)
app.include_router(tipo_almuerzo_router)
app.include_router(almuerzo_router)
app.include_router(pedido_router)
app.include_router(detalle_router)
app.include_router(pago_router)

@app.get("/")
def root():
    return {"message": "API funcionando"}