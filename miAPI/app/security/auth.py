from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials # Importación de HTTPBasic y HTTPBasicCredentials para autenticación básica
import secrets

#Seguridad HTTP Basic --------------------------------------------------------------------------------------------------
security = HTTPBasic()
def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuario_correcto = secrets.compare_digest(credenciales.username, "carmen")
    contrasena_correcta = secrets.compare_digest(credenciales.password, "123456")

    if not (usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas"
        )
    return credenciales.username