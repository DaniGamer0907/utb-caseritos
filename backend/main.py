from fastapi import FastAPI,Depends
from modelos import Proteina
from clases import Proteinas2
from db import get_db
from sqlalchemy.orm import Session

app = FastAPI()

## Clientes
@app.post("/addClient", tags=["Cliente"])
def add_client(cliente: Cliente):
    clientes.append(cliente)
    return {"message": "Cliente agregado correctamente!", "client": cliente}

@app.get("/getClients", tags=["Cliente"])
def get_clients():
    return {"Clientes": clientes}

@app.put("/putCliente", tags=["Cliente"])
def put_cliente(email: str, cliente_update: Cliente):
    for cliente in clientes:
        if cliente.email== email:
            cliente.name = cliente_update.name
            cliente.lastname = cliente_update.lastname
            cliente.address = cliente_update.address
            cliente.phone = cliente_update.phone
            return "Se ha actualizado los datos del cliente correctamente"
    return "No se ha encontrado el cliente con el email ingresado"

@app.delete("/deleteCliente", tags=["Cliente"])
def delete_clientes(email: str):
    for cliente in clientes:
        if cliente.email == email:
            clientes.remove(cliente)
            return "Se ha borrado existosamente"
    return "No se ha encontrado el cliente"


# proteinas
@app.post("/crearProteinas", tags= ["Proteinas"] )
async def crearProteinas(proteinas2: Proteinas2, SessionLocal: Session = Depends(get_db)):
    proteina=Proteina(nombre=proteinas2.nombre, avaliable=proteinas2.avaliable)
    SessionLocal.add(proteina)
    SessionLocal.commit()
    return {"mensaje": "proteina agregado correctamente"}

@app.get("/Proteina", tags=["Proteinas"])
def obtenerProteina():
    return {"Proteina" : Proteinas}

@app.get("/proteinaID" , tags=["Proteinas"])
def obtener_proteina(id: int):
    for proteina in Proteinas:
        if proteina.id_Proteina == id:
            return {"mensaje": "proteina encontrada" , "proteina" :
                     proteina}
        
@app.put("/proteinaID", tags=["Proteinas"])
def actualizarProteinas(id:int, nueva_proteina:Proteina):
    for proteina in Proteinas:
        if proteina.id_Proteina == id:
            proteina.nom_Proteina = nueva_proteina.nom_Proteina
            proteina.disponibilidad = nueva_proteina.disponibilidad
            return {"mensaje": "proteina actualizada correctamente", "proteina": proteina}
    return {"mensaje": "proteina no encontrada"}

@app.delete("/proteinaID", tags=["Proteinas"])
def eliminar_proteina(id: int):
    for proteina in Proteinas:
        if proteina.id_Proteina == id:
            Proteinas.remove(proteina)
            return {"mensaje": "proteina eliminada correctamente"}
    return {"mensaje": "proteina no encontrada"}

## tipo de almuerzo
tipo_almuerzos = []

@app.post("/crearTipoAlmuerzo", tags=["TipoAlmuerzo"])
def crear_tipo_almuerzo(tipo_almuerzo: TipoAlmuerzo):
    tipo_almuerzos.append(tipo_almuerzo)
    return {"mensaje": "Tipo de almuerzo agregado correctamente"}

@app.get("/tipoAlmuerzo", tags=["TipoAlmuerzo"])
def obtener_tipo_almuerzo():
    return {"TipoAlmuerzo": tipo_almuerzos}

@app.get("/tipoAlmuerzoID", tags=["TipoAlmuerzo"])
def obtener_tipo_almuerzo_id(id: int):
    for tipo_almuerzo in tipo_almuerzos:
        if tipo_almuerzo.id_tipo_almuerzo == id:
            return {"mensaje": "Tipo de almuerzo encontrado", "tipo_almuerzo": tipo_almuerzo}
    return {"mensaje": "Tipo de almuerzo no encontrado"}

@app.put("/tipoAlmuerzoID", tags=["TipoAlmuerzo"])
def actualizar_tipo_almuerzo(id: int, nuevo_tipo_almuerzo: TipoAlmuerzo):
    for tipo_almuerzo in tipo_almuerzos:
        if tipo_almuerzo.id_tipo_almuerzo == id:
            tipo_almuerzo.nom_tipo_almuerzo = nuevo_tipo_almuerzo.nom_tipo_almuerzo
            tipo_almuerzo.precio = nuevo_tipo_almuerzo.precio
            return {"mensaje": "Tipo de almuerzo actualizado correctamente", "tipo_almuerzo": tipo_almuerzo}
    return {"mensaje": "Tipo de almuerzo no encontrado"}

@app.delete("/tipoAlmuerzoID", tags=["TipoAlmuerzo"])
def eliminar_tipo_almuerzo(id: int):
    for tipo_almuerzo in tipo_almuerzos:
        if tipo_almuerzo.id_tipo_almuerzo == id:
            tipo_almuerzos.remove(tipo_almuerzo)
            return {"mensaje": "Tipo de almuerzo eliminado correctamente"}
    return {"mensaje": "Tipo de almuerzo no encontrado"}

