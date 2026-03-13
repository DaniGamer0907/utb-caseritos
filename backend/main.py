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
