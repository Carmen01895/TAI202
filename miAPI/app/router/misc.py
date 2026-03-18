from fastapi import FastAPI, APIRouter
from app.data.dtabase import usuarios
from typing import Optional
import asyncio


misc = APIRouter(
    tags = ["Varios"]
)

#Endpoint
@misc.get("/")
async def holamundo():
    return {"mensaje": "Hola, Mundo FasrtAPI"}

@misc.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {"mensaje": "Bienvenido a FastAPI",
            "estatus" : "200",
            }

# ----------------------------------------------------------------------------------------------------------------------

#Endpoint con parametros obligatorios
@misc.get("/v1/parametroOb/{id}")
async def consultauno(id: int):
    return{
        "mensaje":"usuario encontrado",
        "usuario":id,
        "status":"200"
    }

#Endpoint con parametros opcionales
@misc.get("/v1/parametroOp/")
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