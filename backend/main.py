from fastapi import FastAPI,Depends,HTTPException
from modelos import Proteina, Cliente, Almuerzo
from clases import ProteinasC, ClienteC, TipoAlmuerzoC
from db import get_db
from sqlalchemy.orm import Session


app = FastAPI()

## Clientes
@app.post("/addClient", tags=["Cliente"])
def add_client(cliente: ClienteC, db: Session = Depends(get_db)):
    clientedb = Cliente(nombre = cliente.name, lastname = cliente.lastname, address=cliente.address, phone=cliente.phone, email=cliente.email)
    db.add(clientedb)
    db.commit()
    return {"message": "Cliente agregado correctamente!", "client": cliente}

@app.get("/ClienteList", tags=["Cliente"])
def obtenerClientes(db: Session = Depends(get_db)):
    get = db.query(Cliente).all()
    if not get:
        raise HTTPException(status_code=404, detail="Clientes no encontrados")
    else:
        return get

@app.get("/getClients", tags=["Cliente"])
def get_clients(id: int, db: Session = Depends(get_db)):
    get = db.query(Cliente).filter(Cliente.id==id).first()
    if not get:
         raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        return get

@app.put("/putCliente", tags=["Cliente"])
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

@app.delete("/deleteCliente", tags=["Cliente"])
def delete_clientes(id: int, db: Session = Depends(get_db)):
    dbcliente = db.query(Cliente).filter(Cliente.id==id).first()
    if not dbcliente:
         raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        db.delete(dbcliente)
        db.commit()
        return "Se ha borrado existosamente"

# PROTEINAS

@app.post("/crearProteinas", tags= ["Proteinas"] )
def crearProteinas(proteinas: ProteinasC, db: Session = Depends(get_db)):
    proteina=Proteina(nombre=proteinas.nombre, avaliable=proteinas.avaliable)
    db.add(proteina)
    db.commit()
    return {"mensaje": "proteina agregado correctamente"}

@app.get("/ProteinaList", tags=["Proteinas"])
def obtenerProteina(db: Session = Depends(get_db)):
    get = db.query(Proteina).all()
    if not get:
        raise HTTPException(status_code=404, detail="Proteinas no encontradas")
    else:
        return get

@app.get("/proteinaID" , tags=["Proteinas"])
def obtener_proteina(id: int, db: Session = Depends(get_db)):
    get = db.query(Proteina).filter(Proteina.id == id).first()
    if not get:
        raise HTTPException(status_code=404, detail="Proteina no encontrada")
    else:
        return get
        
@app.put("/proteinaID", tags=["Proteinas"])
def actualizarProteinas(id:int, nueva_proteina:ProteinasC, db: Session = Depends(get_db)):
    get = db.query(Proteina).filter(Proteina.id == id).first()
    if not get:
        raise HTTPException(status_code=404, detail="Proteina no encontrada")
    else:
        get.nombre = nueva_proteina.nombre
        get.avaliable = nueva_proteina.avaliable
        db.commit()
        return {"mensaje": "proteina actualizada correctamente", "proteina": nueva_proteina}

@app.delete("/proteinaID", tags=["Proteinas"])
def eliminar_proteina(id: int, db: Session = Depends(get_db)):
    get = db.query(Proteina).filter(Proteina.id == id).first()
    if not get:
        raise HTTPException(status_code=404, detail="Proteina no encontrada")
    else:
        db.delete(get)
        db.commit()
        return {"mensaje": "proteina eliminada correctamente"}

# Tipo de almuerzo

@app.post("/crearTipoAlmuerzo", tags=["TipoAlmuerzo"])
def crear_tipo_almuerzo(tipo_almuerzo: TipoAlmuerzoC, db: Session = Depends(get_db)):
    almuerzodb = Almuerzo(nombre=tipo_almuerzo.nombre, precio=tipo_almuerzo.precio )
    db.add(almuerzodb)
    db.commit()
    return {"mensaje": "Tipo de almuerzo agregado correctamente"}

@app.get("/tipoAlmuerzo", tags=["TipoAlmuerzo"])
def obtener_tipo_almuerzo(db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).all()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzos no encontrados")
    else:
        return almuerzos

@app.get("/tipoAlmuerzoID", tags=["TipoAlmuerzo"])
def obtener_tipo_almuerzo_id(id: int, db: Session=Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        return almuerzos
    
@app.put("/tipoAlmuerzoID", tags=["TipoAlmuerzo"])
def actualizar_tipo_almuerzo(id: int, nuevo_tipo_almuerzo: TipoAlmuerzoC, db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        almuerzos.nombre = nuevo_tipo_almuerzo.nombre
        almuerzos.precio = nuevo_tipo_almuerzo.precio
        db.commit()
        return {"mensaje": "Tipo de almuerzo actualizado correctamente"}
    

@app.delete("/tipoAlmuerzoID", tags=["TipoAlmuerzo"])
def eliminar_tipo_almuerzo(id: int, db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        db.delete(almuerzos)
        db.commit()
        return {"mensaje": "Tipo de almuerzo eliminado correctamente"}
