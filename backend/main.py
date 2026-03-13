from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

clients = []

@app.post("/addClient", tags=["Cliente"])
def add_client(name: str, lastname: str, address:str, phone: str, email: str):
    client = {
        "name": name,
        "lasname":lastname,
        "email": email,
        "address": address,
        "phone": phone,
    }
    clients.append(client)
    return {"message": "Cliente agregado correctamente!", "client": client}

@app.get("/getClients", tags=["Cliente"])
def get_clients():
    return {"Clientes": clients}

@app.put("/putCliente", tags=["Cliente"])
def put_cliente(email: str, cliente_update: dict):
    for cliente in clients:
        if cliente.get("email") == email:
            cliente.update(cliente_update)
            return "Se ha actualizado los datos del cliente correctamente"
    return "No se ha encontrado el cliente con el email ingresado"

@app.delete("/deleteCliente", tags=["Cliente"])
def delete_clientes(email: str):
    for cliente in clients:
        if cliente.get("email") == email:
            clients.remove(cliente)
            return "Se ha borrado existosamente"
    return "No se ha encontrado el cliente"

Proteinas = []

class Proteina(BaseModel):
    id_Proteina : int
    nom_Proteina : str
    cantidad : int


@app.post("/crearProteinas", tags= ["Proteinas"] )
def crearProteinas(Proteina:Proteina):
    Proteinas.append(Proteina)
    return {"mensaje": "proteina agregado correctamente"}


@app.get("/getProteina", tags=["Proteinas"])
def get_Proteina():
    return {"Proteina" : Proteina}

