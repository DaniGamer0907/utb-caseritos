from fastapi import FastAPI

app = FastAPI()

clients = []

@app.post("/addClient", tags=["Cliente"])
def add_client(id: int, name: str, phone: str, email: str):
    client = {
        "id": id,
        "name": name,
        "phone": phone,
        "email": email
    }
    clients.append(client)
    return {"message": "Cliente agregado correctamente!", "client": client}

@app.get("/getClients", tags=["Cliente"])
def get_clients():
    return {"Clientes": clients}


Proteinas = []

class Proteina():
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

