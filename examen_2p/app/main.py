from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field
import asyncio
from typing import Optional 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


app = FastAPI(
    title="Examen 2P - TAI202",
    description="API para el examen de TAI202",
    version="1.0.0"
)

class user(BaseModel):
    nombre: str = Field(..., min_length=6)

class reservas(BaseModel):
    id: int
    fecha: str = Field(..., regex=r"^\d{4}-\d{2}-\d{2}$", gt= "Monday", lt= "Saturday")
    hora: str = Field(..., regex=r"^\d{2}:\d{2}$", gt= "08:00", lt= "22:00")
    personas: int = Field(..., gt=0, lt=10)
    user: user
    confirmacion: Optional[bool] = False

reservas_db = [
    {"id": 1, "fecha": "2026-03-10", "hora": "20:00", "personas": 4, "user": {"nombre": "John Doe"}}
    ]


security = HTTPBasic()
def verificar(credenciales:HTTPBasicCredentials=Depends(security)):
    usuario = secrets.compare_digest(credenciales.username, "admin")
    contrasena = secrets.compare_digest(credenciales.password, "rest123")

    if not (usuario and contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas"
        )
    return credenciales.username

# Crear reserva
@app.post("/reservas", tags=["Reservas"], status_code=status.HTTP_201_CREATED)
async def crear(reserva:reservas): 
    for l in reservas_db:
        if l["id"] == reserva.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de reserva ya existe")

    reservas_db.append(reserva.dict())
    return {"mensaje": "Reserva creada exitosamente", "reserva": reserva}

# Listar Reservas
@app.get("/reservas/listar", tags=["Reservas"])
async def listar(usuarioAuth:str = Depends()):
    return {
        "total": len(reservas_db),
        "reservas": reservas_db
        }

# Consultar por ID
@app.get("/reservas/{reserva_id}", tags=["Reservas"], status_code= status.HTTP_200_OK)
async def consultar(reserva_id: int):
    for reserva in reservas_db:
        if reserva["id"] == reserva_id:
            return reserva
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")

#Confirmar reserva
@app.post("/reservas/{reserva_id}/confirmar", tags=["Reservas"], status_code=status.HTTP_200_OK)
async def confirmar(reserva_id: int, usuario: str = Depends(verificar)):
    for reserva in reservas_db:
        if reserva["id"] == reserva_id:
            if reserva["confirmacion"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reserva ya confirmada")
            reserva["confirmacion"] = True
            return {"mensaje": "Reserva confirmada exitosamente", "reserva": reserva}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")

#Cancelar reserva
@app.delete("/reservas/{reserva_id}", tags=["Reservas"], status_code=status.HTTP_200_OK)
async def cancelar(reserva_id: int, usuarioAuth: str = Depends(verificar)):
    for reserva in reservas_db:
        if reserva["id"] == reserva_id:
            reservas_db.remove(reserva)
            return {"mensaje": "Reserva cancelada exitosamente"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")