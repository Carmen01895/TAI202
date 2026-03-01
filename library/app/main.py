# Importaciones
from fastapi import FastAPI, status, HTTPException
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Instancia del servidor
app = FastAPI(
    title="Biblioteca Digital",
    description="Repaso - Práctica 5",
    version="1.0.0"
)

# Pydantic models

class Libro(BaseModel):
    id: int
    titulo: str = Field(..., min_length=2, max_length=100) 
    autor: str
    anio: int = Field(..., gt=1450, le=datetime.now().year) 
    paginas: int = Field(..., gt=1) 
    estado: Literal["disponible", "prestado"] = "disponible"

class Usuario(BaseModel):
    nombre: str
    correo: EmailStr 

class Prestamo(BaseModel):
    id_prestamo: int
    id_libro: int
    usuario: Usuario

# Tablas simuladas

libros = [
    {"id": 1, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "anio": 1967, "paginas": 471, "estado": "disponible"},
    {"id": 2, "titulo": "El Principito", "autor": "Antoine de Saint-Exupéry", "anio": 1943, "paginas": 96, "estado": "disponible"}
]

prestamos = []

# Endpoints--------------------------------------------------------------------

#Registrar un libro 
@app.post("/v1/libros/", tags=['Libros'], status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro: Libro):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=400, detail="Hay un libro registrado con ese ID")
    
    libros.append(libro.model_dump())
    return {"mensaje": "El libro ha sido registrado con éxito", "libro": libro}

#Listar todos los libros
@app.get("/v1/libros/disponibles", tags=['Libros'])
async def listar_libros():
    return {
        "total": len(libros),
        "libros": libros
    }

#Buscar un libro por su nombre
@app.get("/v1/libros/buscar", tags=['Libros'])
async def buscar_libro(nombre: str):
    resultados = [l for l in libros if nombre.lower() in l["titulo"].lower()]
    if not resultados:
        raise HTTPException(status_code=404, detail="No hay libros con ese nombre")
    return {"resultados": resultados}

#Registrar el préstamo de un libro
@app.post("/v1/prestamos/", tags=['Préstamos'], status_code=status.HTTP_201_CREATED)
async def registrar_prestamo(prestamo: Prestamo):
    libro_encontrado = None
    for l in libros:
        if l["id"] == prestamo.id_libro:
            libro_encontrado = l
            break
    
    if not libro_encontrado:
        raise HTTPException(status_code=404, detail="El libro no ha sido encontrado")
    
    if libro_encontrado["estado"] == "prestado":
        raise HTTPException(status_code=409, detail="El libro se encuentra actualmente prestado")

    libro_encontrado["estado"] = "prestado"
    prestamos.append(prestamo.model_dump())
    
    return {"mensaje": "Préstamo registrado", "detalle": prestamo}

# Marcar un libro como devuelto
@app.patch("/v1/libros/devolver/{id_libro}", tags=['Préstamos'])
async def devolver_libro(id_libro: int):
    for l in libros:
        if l["id"] == id_libro:
            if l["estado"] == "disponible":
                return {"mensaje": "El libro ya estaba en biblioteca"}
            
            l["estado"] = "disponible"
            return {"mensaje": "Libro devuelto", "status": "200"}
            
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Eliminar el registro de un préstamo
@app.delete("/v1/prestamos/{id_prestamo}", tags=['Préstamos'])
async def eliminar_prestamo(id_prestamo: int):
    for idx, p in enumerate(prestamos):
        if p["id_prestamo"] == id_prestamo:
            id_libro = p["id_libro"]
            for l in libros:
                if l["id"] == id_libro:
                    l["estado"] = "disponible"
            
            prestamos.pop(idx)
            return {"mensaje": "Registro de préstamo eliminado"}
    
    raise HTTPException(status_code=409, detail="El registro de préstamo ya no existe")