from pydantic import BaseModel, Field 

class crear_usuario(BaseModel):
    id: int = Field(..., description="Identificador")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, descriprion="Edad valida entre 1 y 123")