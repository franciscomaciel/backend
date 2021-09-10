from pydantic import BaseModel


class UsuarioSimples(BaseModel):
    login_AD: str


class Usuario(BaseModel):
    login_AD: str
    password: str


class LoginData(BaseModel):
    login_AD: str
    password: str


class LoginSuccessful(BaseModel):
    user: UsuarioSimples
    access_token: str


class SchemaLiberarPedido(BaseModel):
    numero_pedido_filial : str
    codigo_usuario_liberador : str
    justificativa : str


class SchemaLiberarItemPedido(BaseModel):
    numero_pedido_filial : str
    codigo_usuario_liberador : str
    justificativa : str
    item_bloqueio : str