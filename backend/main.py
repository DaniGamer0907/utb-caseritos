from fastapi import FastAPI

app = FastAPI()

client = []

@app.post("/addUser", tags=["Cliente"])
def add_user(id: int, name: str, phone: str, email: str):
    user = {
        "id": id,
        "name": name,
        "phone": phone,
        "email": email
    }
    client.append(user)
    return {"message": "User added successfully", "user": user}

@app.get("/getUsers", tags=["Cliente"])
def get_users():
    return {"users": client}
