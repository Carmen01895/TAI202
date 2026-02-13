#importaciones
from fastapi import FastAPI, Query
import asyncio

#Instancia del servidor
app = FastAPI()

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

#Endpoint con parametros obligatorios

@app.get("/obligatorios")
def obligatorios(nombre: str = Query(..., description="Nombre Obligatorio"), edad: int = 
                 Query(..., description="Edad Obligatoria")):
    return {"mensaje": f"Hola {nombre}, tu edad es {edad}"}

#Endpoint con parametros opcionales

@app.get("/opcionales")
def opcionales(cidad: str = Query(None, description="Ciudad Opcional"), pais: str = Query(None, description="Pais Opcional")):
    return {
        "mensaje": "Datos recibidos",
        "ciudad": cidad or "No especificado",
        "pais": pais or "No especificado"
    }