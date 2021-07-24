"""
    models.py
    Classes utilizadas para receber e enviar dados pela API REST criada com o FastAPI.
    Author: Francisco Maciel
    Data: 20/12/2020
    Alterações:
    30/01/2021 - Mantido(s) apenas o(s) modelo(s) necessário(s) à comunicação entre a API e o front-end - eliminados
                 modelos redundantes, pois não será usado o modelo ORM do SQLAlchemy.
"""

from pydantic import BaseModel

"""
    Modelo usado para receber as informações usadas para liberar um pedido. 
"""
class ModeloLiberarPedido(BaseModel):
    numero_pedido_filial: str
    codigo_usuario_liberador: str
    justificativa: str


class ModeloLiberarItemPedido(BaseModel):
    numero_pedido_filial: str
    codigo_usuario_liberador: str
    justificativa: str
    item_bloqueio: str


"""
class ModeloObterBloqueios(BaseModel):
    numero_pedido_filial: str


class ModeloObterItensPedido(BaseModel):
    numero_pedido_filial: str
"""