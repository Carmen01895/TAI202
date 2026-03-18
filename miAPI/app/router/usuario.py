from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.dtabase import usuarios
from app.security.auth import verificar_peticion

router = APIRouter(
    prefix='/v1/usuarios',
    tags='CRUD HTTP'
)

#GET
@router.get("/")
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
        }

#POST
@router.post("/", status_code=status.HTTP_201_CREATED)
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
@router.put("/{id}")
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
@router.patch("/{id}")
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
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAuth:str = Depends(verificar_peticion)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(idx)
            return {
                "mensaje": f"usuario eliminado por {usuarioAuth}",
                "id eliminado": id
            }
    raise HTTPException(
        status_code=404, 
        detail="usuario no encontrado")