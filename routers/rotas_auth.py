from fastapi import APIRouter, status, Depends, HTTPException
from schemas.schemas import Usuario, UsuarioSimples
from starlette import status
from ..infra.providers import hash_provider


router = APIRouter()

@router.post('/signup',
             status_code=status.HTTP_201_CREATED,
             response_model=UsuarioSimples)
def signup(usuario: Usuario):
    usuario_criado = None   # TODO: Implementar
    return usuario_criado