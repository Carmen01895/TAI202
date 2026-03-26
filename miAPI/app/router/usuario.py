from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.dtabase import usuarios
from app.security.auth import verificar_peticion

#Importaciones de BD
from sqlalchemy.orm import Session
from app.data.db import get_db 
from app.data.usuarios import usuario as dbusuario

router = APIRouter(
    prefix='/v1/usuarios',
    tags=['CRUD HTTP']
)

#GET
@router.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    queryUsuarios= db.query(dbusuario).all()
    return {
        "total": len(queryUsuarios),
        "usuarios": queryUsuarios,
        "status": "200"
        }

#GET por ID
@router.get("/{id}")
async def leer_usuario(id: int, db: Session = Depends(get_db)):
    usuario= db.query(dbusuario).filter(dbusuario.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    return {
        "usuario": usuario,
        "status": "200"
    }

#POST
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_nuevo_usuario(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    nuevoU= dbusuario(
        nombre=usuarioP.nombre,
        edad=usuarioP.edad
    )
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)
    return {
        "mensaje": "Usuario Agregado",
        "Usuario": usuarioP
    }

#PUT
@router.put("/{id}")
async def actualizar_usuario(id: int, usuario_update: crear_usuario, db: Session = Depends(get_db)):
    usuario = db.query(dbusuario).filter(dbusuario.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    usuario.nombre = usuario_update.nombre
    usuario.edad = usuario_update.edad
    db.commit()
    db.refresh(usuario)
    return {
        "mensaje": "usuario actualizado",
                "datos nuevos": usuario
            }

#PATCH
@router.patch("/{id}")
async def modificar_usuario(id: int, cambios: dict, db: Session = Depends(get_db)):
    usuario = db.query(dbusuario).filter(dbusuario.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return {
        "mensaje": "usuario modificado",
                "datos actualizados": usuario
            }

#DELETE
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAuth:str = Depends(verificar_peticion), db: Session = Depends(get_db)):
    usuario = db.query(dbusuario).filter(dbusuario.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    db.delete(usuario)
    db.commit()
    return {
        "mensaje": f"usuario eliminado por {usuarioAuth}",
                "id eliminado": id
            }