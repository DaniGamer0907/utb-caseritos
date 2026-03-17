from fastapi import FastAPI,Depends,HTTPException
from modelos import Proteina, Cliente, TipoAlmuerzo, Pedido, Almuerzo, DetallePedidos, Pago
from clases import ProteinasC, ClienteC, TipoAlmuerzoC, PedidoC, AlmuerzoC, DetallePedidosC, PagoC
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
    almuerzodb = TipoAlmuerzo(nombre=tipo_almuerzo.nombre, precio=tipo_almuerzo.precio )
    db.add(almuerzodb)
    db.commit()
    return {"mensaje": "Tipo de almuerzo agregado correctamente"}

@app.get("/tipoAlmuerzo", tags=["TipoAlmuerzo"])
def obtener_tipo_almuerzo(db: Session = Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).all()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzos no encontrados")
    else:
        return almuerzos

@app.get("/tipoAlmuerzoID", tags=["TipoAlmuerzo"])
def obtener_tipo_almuerzo_id(id: int, db: Session=Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        return almuerzos
    
@app.put("/tipoAlmuerzoID", tags=["TipoAlmuerzo"])
def actualizar_tipo_almuerzo(id: int, nuevo_tipo_almuerzo: TipoAlmuerzoC, db: Session = Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        almuerzos.nombre = nuevo_tipo_almuerzo.nombre
        almuerzos.precio = nuevo_tipo_almuerzo.precio
        db.commit()
        return {"mensaje": "Tipo de almuerzo actualizado correctamente"}
    

@app.delete("/tipoAlmuerzoID", tags=["TipoAlmuerzo"])
def eliminar_tipo_almuerzo(id: int, db: Session = Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        db.delete(almuerzos)
        db.commit()
        return {"mensaje": "Tipo de almuerzo eliminado correctamente"}

# Pedido

@app.post("/crearPedido", tags=["Pedidos"])
def crear_pedido(pedido: PedidoC, db: Session = Depends(get_db)):
    pedidodb = Pedido(fecha_creacion=pedido.fecha_creacion, estado=pedido.estado, sugerencia=pedido.sugerencia)
    db.add(pedidodb)
    db.commit()
    return {"mensaje": "Pedido agregado correctamente"}

@app.get("/Pedido", tags=["Pedidos"])
def obtener_pedido(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).all()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedidos no encontrados")
    else:
        return pedidos

@app.get("/PedidoID", tags=["Pedidos"])
def obtener_pedido_id(id: int, db: Session=Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    else:
        return pedidos
    
@app.put("/PedidoID", tags=["Pedidos"])
def actualizar_pedido(id: int, nuevo_pedido: PedidoC, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    else:
        pedidos.fecha_creacion = nuevo_pedido.fecha_creacion
        pedidos.estado = nuevo_pedido.estado
        pedidos.sugerencia = nuevo_pedido.sugerencia
        db.commit()
        return {"mensaje": "Pedido actualizado correctamente"}
    

@app.delete("/PedidoID", tags=["Pedidos"])
def eliminar_pedido(id: int, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    else:
        db.delete(pedidos)
        db.commit()
        return {"mensaje": "Pedido eliminado correctamente"}

# Almuerzo

@app.post("/crearAlmuerzo", tags=["Almuerzos"])
def crear_almuerzo(almuerzo: AlmuerzoC, db: Session = Depends(get_db)):
    almuerzodb = Almuerzo(descripcion=almuerzo.descripcion, fecha=almuerzo.fecha)
    db.add(almuerzodb)
    db.commit()
    return {"mensaje": "Almuerzo agregado correctamente"}

@app.get("/Almuerzo", tags=["Almuerzos"])
def obtener_almuerzo(db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).all()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzos no encontrados")
    else:
        return almuerzos

@app.get("/AlmuerzoID", tags=["Almuerzos"])
def obtener_almuerzo_id(id: int, db: Session=Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        return almuerzos
    
@app.put("/AlmuerzoID", tags=["Almuerzos"])
def actualizar_almuerzo(id: int, nuevo_almuerzo: AlmuerzoC, db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        almuerzos.descripcion=nuevo_almuerzo.descripcion
        almuerzos.fecha=nuevo_almuerzo.fecha
        db.commit()
        return {"mensaje": "Almuerzo actualizado correctamente"}
    

@app.delete("/AlmuerzoID", tags=["Almuerzos"])
def eliminar_almuerzo(id: int, db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        db.delete(almuerzos)
        db.commit()
        return {"mensaje": "Almuerzo eliminado correctamente"}

# Detalle de Pedidos

@app.post("/crearDetallePedidos", tags=["DetallePedidos"])
def crear_detalle_pedido(detalle_pedido: DetallePedidosC, db: Session = Depends(get_db)):
    pedidodb = DetallePedidos(cantidad=detalle_pedido.cantidad, precio_unitario=detalle_pedido.precio_unitario, total=detalle_pedido.total )
    db.add(pedidodb)
    db.commit()
    return {"mensaje": "Detalle de Pedido agregado correctamente"}

@app.get("/DetallePedidos", tags=["DetallePedidos"])
def obtener_detalle_pedido(db: Session = Depends(get_db)):
    pedidos = db.query(DetallePedidos).all()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedidos no encontrados")
    else:
        return pedidos

@app.get("/DetallePedidosID", tags=["DetallePedidos"])
def obtener_detalle_pedido_id(id: int, db: Session=Depends(get_db)):
    pedidos = db.query(DetallePedidos).filter(DetallePedidos.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        return pedidos
    
@app.put("/DetallePedidosID", tags=["DetallePedidos"])
def actualizar_detalle_pedido(id: int, nuevo_detalle_pedido: DetallePedidosC, db: Session = Depends(get_db)):
    pedidos = db.query(DetallePedidos).filter(DetallePedidos.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        pedidos.cantidad = nuevo_detalle_pedido.cantidad
        pedidos.precio_unitario = nuevo_detalle_pedido.precio_unitario
        pedidos.total = nuevo_detalle_pedido.total
        db.commit()
        return {"mensaje": "Detalle de Pedido actualizado correctamente"}
    

@app.delete("/DetallePedidosID", tags=["DetallePedidos"])
def eliminar_detalle_pedido(id: int, db: Session = Depends(get_db)):
    pedidos = db.query(DetallePedidos).filter(DetallePedidos.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        db.delete(pedidos)
        db.commit()
        return {"mensaje": "Detalle de Pedido eliminado correctamente"}

# Pago

@app.post("/crearPago", tags=["Pago"])
def crear_pago(pago: PagoC, db: Session = Depends(get_db)):
    pagodb = Pago(metodopago=pago.metodopago, diadelpago=pago.diadelpago )
    db.add(pagodb)
    db.commit()
    return {"mensaje": "Pago agregado correctamente"}

@app.get("/Pago", tags=["Pago"])
def obtener_pago(db: Session = Depends(get_db)):
    pagos = db.query(Pago).all()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pagos no encontrados")
    else:
        return pagos

@app.get("/PagoID", tags=["Pago"])
def obtener_pago_id(id: int, db: Session=Depends(get_db)):
    pagos = db.query(Pago).filter(Pago.id==id).first()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        return pagos
    
@app.put("/PagoID", tags=["Pago"])
def actualizar_pago(id: int, nuevo_pago: PagoC, db: Session = Depends(get_db)):
    pagos = db.query(Pago).filter(Pago.id==id).first()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        pagos.metodopago = nuevo_pago.metodopago
        pagos.diadelpago = nuevo_pago.diadelpago
        db.commit()
        return {"mensaje": "Pago actualizado correctamente"}
    

@app.delete("/PagoID", tags=["Pago"])
def eliminar_pago(id: int, db: Session = Depends(get_db)):
    pagos = db.query(Pago).filter(Pago.id==id).first()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        db.delete(pagos)
        db.commit()
        return {"mensaje": "Pago eliminado correctamente"}

