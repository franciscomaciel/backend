"""
    schemas.py
    Classes utilizadas para receber e enviar dados pela API REST criada com o FastAPI.
    Author: Francisco Maciel
    Data: 20/12/2020
"""

from pydantic import BaseModel

"""
    Modelo usado para receber as informações usadas para liberar um pedido. 
"""
class ModeloLiberarPedido(BaseModel):
    numero_pedido_filial: str
    codigo_usuario_liberador: str
    justificativa: str


"""
    Modelo usado para receber as informações usadas para liberar um *item* de pedido. 
"""
class ModeloLiberarItemPedido(BaseModel):
    numero_pedido_filial: str
    codigo_usuario_liberador: str
    justificativa: str
    item_bloqueio: str

"""
    Modelo usado para passar credenciais ao OAuth2. 
"""
class AuthDetails(BaseModel):
    username: str
    password: str
