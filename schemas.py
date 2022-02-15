from pydantic import BaseModel


class _UserBase(BaseModel):
    login_ad: str


# DTO usado para passar parâmetros para a criação de um usuário no SGBD.
class UserCreate(_UserBase):
    senha: str

    class Config:
        orm_mode = True


# Representa um usuário que já foi persistido no SGBD.
class User(_UserBase):
    # id: int   - será necessário ?
    hash_senha: str

    class Config:
        orm_mode = True


class LoginSucesso(BaseModel):
    usuario: _UserBase
    access_token: str


class SchemaLiberarPedido(BaseModel):
    numero_pedido_filial: str
    codigo_usuario_liberador: str
    justificativa: str


class SchemaLiberarItemPedido(BaseModel):
    numero_pedido_filial: str
    codigo_usuario_liberador: str
    justificativa: str
    item_bloqueio: str
