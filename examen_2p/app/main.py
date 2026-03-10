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

security = HTTPBasic()
def verficar(credenciales:HTTPBasicCredentials=Depends(security)):
    usuario = secrets.compare_digest(credenciales.username, "admin")
    contrasena = secrets.compare_digest(credenciales.password, "admin123")

    if not (usuario and contrasena):
