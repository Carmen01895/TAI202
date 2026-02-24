#importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field 

#Instancia del servidor
app = FastAPI(
    title="Mi Primer API",
    description="María Carmen Atilano García",
    version="1.0"
)

#Endpoint
@app.get("/")
async def holamundo():
    return {"mensaje": "Hola, Mundo FasrtAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {"mensaje": "Bienvenido a FastAPI",
            "estatus" : "200",
            }

#Tabla ficticia
usuarios = [
    {"id": 1, "nombre": "Fanny", "edad": 21},
    {"id": 2, "nombre": "Aly", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21}
]

class crear_usuario(BaseModel):
    id: int = Field(..., description="Identificador")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, descriprion="Edad valida entre 1 y 123")

#Endpoint con parametros obligatorios
@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def consultauno(id: int):
    return{
        "mensaje":"usuario encontrado",
        "usuario":id,
        "status":"200"
    }

#Endpoint con parametros opcionales
@app.get("/v1/parametroOp/", tags=['Parametro Opcional'])
async def consultados(id: Optional [int]=None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return{
                    "mensaje":"usuario encontrado",
                    "usuario":usuarioK
                }
        return{
            "mensaje":"usuario no encontrado",
            "status":"200"
        }
    else:
        return{
            "mensaje":"No se proporciono id",
            "status":"200"
        }

#GET
@app.get("/v1/usuarios", tags=['HTTP CRUD'])
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
        }

#POST
@app.post("/v1/usuarios/", tags=['HTTP CRUD'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje": "Usuario Agregado",
        "Usuario": usuario
    }

#PUT
@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario(id: int, usuario: dict):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[idx] = usuario
            return {
                "mensaje": "usuario actualizado",
                "datos nuevos": usuario
            }
    raise HTTPException(
        status_code=404, 
        detail="usuario no encontrado")

#PATCH
@app.patch("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def modificar_usuario(id: int, cambios: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(cambios)
            return {
                "mensaje": "usuario modificado",
                "datos actualizados": usr
            }
    raise HTTPException(
        status_code=404, 
        detail="usuario no encontrado")

#DELETE
@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(idx)
            return {
                "mensaje": "usuario eliminado",
                "id eliminado": id
            }
    raise HTTPException(
        status_code=404, 
        detail="usuario no encontrado")


