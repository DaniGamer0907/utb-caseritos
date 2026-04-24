# UTB Caseritos

Aplicacion web para gestionar y promocionar el restaurante **Caseritos**. El proyecto esta dividido en un frontend en Angular y un backend en FastAPI con autenticacion JWT y persistencia en PostgreSQL.

## Arquitectura

- `frontend/`: interfaz web en Angular 21.
- `backend/`: API REST en FastAPI.
- `backend/models/`: modelos SQLAlchemy.
- `backend/routes/`: rutas para autenticacion y CRUD del sistema.
- `backend/schemas/`: esquemas Pydantic para validacion de datos.

## Funcionalidades actuales

- Inicio de sesion con JWT.
- Registro de usuarios.
- Vista publica tipo landing page para el restaurante.
- CRUD base para usuarios, proteinas, tipos de almuerzo, almuerzos, pedidos, detalles de pedido y pagos.
- Validaciones de acceso por rol en algunas rutas del backend.

## Tecnologias

### Frontend

- Angular 21
- TypeScript
- Bootstrap 5

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Passlib
- Python-Jose
- Python-Dotenv

## Requisitos

- Node.js y npm
- Python 3.10 o superior
- PostgreSQL

## Variables de entorno del backend

El backend depende de un archivo `.env` dentro de `backend/` o de variables de entorno equivalentes.

```env
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tu_base_de_datos
SECRET_KEY=una_clave_secreta
ALGORITHM=HS256
EXPIRE_MINUTES=60
```

## Instalacion

### 1. Frontend

```bash
cd frontend
npm install
```

### 2. Backend

Las dependencias Python del backend estan definidas en `requirements.txt` en la raiz del proyecto.

```bash
python -m pip install -r requirements.txt
```

Opcionalmente, puedes crear y activar un entorno virtual antes de instalar dependencias.

## Ejecucion en desarrollo

### Backend

Desde la carpeta `backend/`:

```bash
uvicorn main:app --reload
```

La API queda disponible en:

- `http://localhost:8000/`
- `http://localhost:8000/docs`

### Frontend

Desde la carpeta `frontend/`:

```bash
npm start
```

La aplicacion queda disponible en:

- `http://localhost:4200/`

## Integracion frontend-backend

- El frontend consume autenticacion en `http://localhost:8000/auth`.
- El backend permite CORS para `http://localhost:4200`.
- Si cambias puertos o dominios, debes actualizar ambos lados.

## Rutas principales del frontend

- `/`: login
- `/Registrar`: registro de usuario
- `/home`: pagina principal del restaurante

## Rutas principales del backend

### Autenticacion

- `POST /auth/login`
- `POST /auth/registro`

### Modulos CRUD

- `/usuario`
- `/proteina`
- `/tipoalmuerzo`
- `/almuerzo`
- `/pedido`
- `/detallesPedido`
- `/Pago`

## Modelo de dominio

Las entidades principales del sistema son:

- `Usuario`
- `Rol`
- `Proteina`
- `TipoAlmuerzo`
- `Almuerzo`
- `Pedido`
- `DetallePedido`
- `Pago`

## Notas importantes

- Las tablas se crean automaticamente al iniciar el backend con `Base.metadata.create_all(bind=engine)`.
- La ruta raiz del backend responde con `{"message": "API funcionando"}`.
- El login espera credenciales en formato `application/x-www-form-urlencoded`.
- El proyecto contiene algunos textos con problemas de codificacion en la interfaz y en respuestas del backend; no afecta este README, pero conviene corregirlo despues.

## Estructura del proyecto

```text
utb-caseritos/
|-- backend/
|   |-- auth/
|   |-- models/
|   |-- routes/
|   |-- schemas/
|   |-- db.py
|   `-- main.py
|-- frontend/
|   |-- src/
|   |-- angular.json
|   `-- package.json
`-- README.md
```

## Estado actual

El repositorio ya tiene la base funcional para autenticacion, gestion de usuarios y administracion de almuerzos y pedidos, pero todavia requiere estandarizar dependencias, mejorar validaciones y completar documentacion tecnica mas detallada si se va a desplegar o mantener en equipo.
