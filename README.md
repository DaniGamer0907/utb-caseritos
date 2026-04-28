# UTB Caseritos

Sistema web para el restaurante **Caseritos**. El repositorio esta dividido en tres capas:

- **Frontend** en Angular, desplegado en **Vercel**.
- **API** en FastAPI, desplegada en **Render**.
- **Base de datos** PostgreSQL administrada en **Supabase**.

La aplicacion permite ver el menu, autenticarse, registrar usuarios y gestionar pedidos desde el backend.

## Arquitectura

```text
frontend/  -> Angular 21 + SSR
backend/   -> FastAPI + SQLAlchemy + JWT
Supabase   -> PostgreSQL
Render     -> API publica
Vercel     -> Frontend publico
```

## Flujo general

1. El usuario entra al frontend publicado en Vercel.
2. El frontend consulta la API hospedada en Render.
3. La API valida autenticacion con JWT y aplica reglas por rol.
4. Los datos se guardan y leen desde PostgreSQL en Supabase.

## Tecnologias

### Frontend

- Angular 21
- TypeScript
- Angular Material
- Bootstrap 5

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT con `python-jose`
- Hash de contrasenas con `passlib`

### Infraestructura

- Supabase para la base de datos
- Render para la API
- Vercel para el frontend

## Estructura del proyecto

### `backend/`

- `main.py`: arranque de la API, CORS y registro de rutas.
- `db.py`: conexion a PostgreSQL usando variables de entorno.
- `models/`: modelos ORM de SQLAlchemy.
- `routes/`: endpoints REST.
- `schemas/`: validacion de entrada y salida con Pydantic.
- `auth/`: hashing, JWT y dependencias de autenticacion.

### `frontend/`

- `src/app/components/`: vistas principales como login, registro y home.
- `src/app/services/`: servicios para consumir la API.
- `src/app/guards/`: proteccion de rutas.
- `src/app/admin/`: modulo administrativo cargado por lazy loading.
- `src/app/services/api/api-config.ts`: URL base de la API desplegada.

## Funcionalidades

- Inicio de sesion con JWT.
- Registro de usuarios.
- Visualizacion del menu del restaurante.
- Gestion de pedidos.
- Administracion de productos relacionados con el menu.
- Control de acceso por rol para rutas administrativas.

## Rutas principales del frontend

- `/`: pagina principal.
- `/logni`: login.
- `/registrar`: registro.
- `/admin`: area administrativa protegida.

## Rutas principales del backend

### Salud

- `GET /` -> verifica que la API este activa.

### Autenticacion

- `POST /auth/login`
- `POST /auth/registro`

### Recursos

- `/usuario`
- `/proteina`
- `/tipoalmuerzo`
- `/pedido`
- `/detallesPedido`
- `/Pago`

## Base de datos

La base de datos es PostgreSQL en Supabase. El backend se conecta mediante variables de entorno y crea las tablas al iniciar con `Base.metadata.create_all(bind=engine)`.

Entidades principales:

- `Usuario`
- `Rol`
- `Proteina`
- `TipoAlmuerzo`
- `Pedido`
- `DetallePedido`
- `Pago`

## Variables de entorno

### Backend `backend/.env`

```env
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=tu-host.supabase.co
DB_PORT=5432
DB_NAME=tu_base_de_datos
SECRET_KEY=una_clave_secreta
ALGORITHM=HS256
EXPIRE_MINUTES=60
CORS_ORIGINS=https://tu-frontend.vercel.app,http://localhost:4200
```

### Frontend

La URL de la API se define en:

- `frontend/src/app/services/api/api-config.ts`

Actualmente apunta a:

```ts
export const API_BASE_URL = 'https://utb-caseritos.onrender.com';
```

Si cambias el dominio de Render, actualiza ese archivo.

## Instalacion local

### 1. Clonar e instalar frontend

```bash
cd frontend
npm install
```

### 2. Instalar backend

Desde la carpeta `backend/`:

```bash
python -m pip install -r requirements.txt
```

## Ejecucion local

### Backend

Desde `backend/`:

```bash
uvicorn main:app --reload
```

La API queda disponible en:

- `http://localhost:8000`
- `http://localhost:8000/docs`

### Frontend

Desde `frontend/`:

```bash
npm start
```

La aplicacion queda disponible en:

- `http://localhost:4200`

## Despliegue

### Render

La API se despliega como servicio web en Render. Debe tener configuradas las variables de entorno del backend y el comando de arranque correspondiente a FastAPI/uvicorn.

### Supabase

Supabase hospeda la base de datos PostgreSQL. El backend usa la cadena de conexion configurada en `backend/.env`.

### Vercel

El frontend se publica en Vercel. Debe apuntar a la URL publica de la API en Render.

## Autenticacion y roles

- El login usa `application/x-www-form-urlencoded`.
- El backend retorna un `access_token` JWT y el rol del usuario.
- El frontend guarda `token` y `role` en `localStorage`.
- Las rutas administrativas usan guards para bloquear acceso sin sesion o sin rol `admin`.

## Notas tecnicas

- El backend habilita CORS para los orígenes definidos en `CORS_ORIGINS`.
- La API crea tablas automaticamente al iniciar.
- El proyecto contiene archivos generados por Angular y Python cacheados localmente; no forman parte de la logica del sistema.

## Estado del proyecto

El repositorio ya tiene una base funcional para autenticacion, catalogo y pedidos. Si se va a mantener en equipo, el siguiente paso razonable es centralizar las URLs de entorno, estandarizar nombres de rutas y documentar el contrato de cada endpoint.
