from fastapi import APIRouter
from starlette import status
from ..infra.providers import hash_provider

from schemas.schemas import Usuario, UsuarioSimples

router = APIRouter()

@router.post('/signup',
             status_code=status.HTTP_201_CREATED,
             response_model=UsuarioSimples)
def signup(usuario: Usuario):
    usuario.password = hash_provider.gerar_hash(usuario.password)
    usuario_criado = None   # TODO: Implementar
    return usuario_criado