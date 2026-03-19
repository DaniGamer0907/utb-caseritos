from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Cliente import Cliente
from schemas.Cliente_schemas import ClienteC

router= APIRouter(prefix="/Cliente", tags= ["Client"])


@router.post("/addClient")
def add_client(cliente: ClienteC, db: Session = Depends(get_db)):
    clientedb = Cliente(nombre = cliente.name, lastname = cliente.lastname, address=cliente.address, phone=cliente.phone, email=cliente.email)
    db.add(clientedb)
    db.commit()
    return {"message": "Cliente agregado correctamente!", "client": cliente}

@router.get("/ClienteList")
def obtenerClientes(db: Session = Depends(get_db)):
    get = db.query(Cliente).all()
    if not get:
        raise HTTPException(status_code=404, detail="Clientes no encontrados")
    else:
        return get

@router.get("/getClients")
def get_clients(id: int, db: Session = Depends(get_db)):
    get = db.query(Cliente).filter(Cliente.id==id).first()
    if not get:
         raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        return get

@router.put("/putCliente")
def put_cliente(id: int, cliente_update: ClienteC, db: Session = Depends(get_db)):
    dbcliente = db.query(Cliente).filter(Cliente.id==id).first()
    if not dbcliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        dbcliente.nombre = cliente_update.name
        dbcliente.lastname = cliente_update.lastname
        dbcliente.address = cliente_update.address
        dbcliente.phone = cliente_update.phone
        dbcliente.email = cliente_update.email
        db.commit()
        return "Se ha actualizado los datos del cliente correctamente"

@router.delete("/deleteCliente")
def delete_clientes(id: int, db: Session = Depends(get_db)):
    dbcliente = db.query(Cliente).filter(Cliente.id==id).first()
    if not dbcliente:
         raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        db.delete(dbcliente)
        db.commit()
        return "Se ha borrado existosamente"



