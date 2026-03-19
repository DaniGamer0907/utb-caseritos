from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Cliente import Cliente
from schemas.Cliente_schemas import ClienteC

router= APIRouter(prefix="/cliente", tags= ["Clientes"])


@router.post("/addCliente")
def agregar_cliente(cliente: ClienteC, db: Session = Depends(get_db)):
    clientedb = Cliente(nombre = cliente.name, lastname = cliente.lastname, address=cliente.address, phone=cliente.phone, email=cliente.email)
    db.add(clientedb)
    db.commit()
    return {"message": "Cliente agregado correctamente!", "client": cliente}

@router.get("/listClientes")
def obtener_Clientes(db: Session = Depends(get_db)):
    get = db.query(Cliente).all()
    if not get:
        raise HTTPException(status_code=404, detail="Clientes no encontrados")
    else:
        return get

@router.get("/getCliente")
def obtener_cliente(id: int, db: Session = Depends(get_db)):
    get = db.query(Cliente).filter(Cliente.id==id).first()
    if not get:
         raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        return get

@router.put("/actualizarCliente")
def actualizar_cliente(id: int, cliente_update: ClienteC, db: Session = Depends(get_db)):
    dbcliente = db.query(Cliente).filter(Cliente.id==id).first()
    if not dbcliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        dbcliente.nombre = cliente_update.name #type: ignore
        dbcliente.lastname = cliente_update.lastname #type: ignore
        dbcliente.address = cliente_update.address #type: ignore
        dbcliente.phone = cliente_update.phone #type: ignore
        dbcliente.email = cliente_update.email #type: ignore
        db.commit()
        return "Se ha actualizado los datos del cliente correctamente"

@router.delete("/deleteCliente")
def borrar_cliente(id: int, db: Session = Depends(get_db)):
    dbcliente = db.query(Cliente).filter(Cliente.id==id).first()
    if not dbcliente:
         raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        db.delete(dbcliente)
        db.commit()
        return "Se ha borrado existosamente"



