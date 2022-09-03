import fastapi as _fastapi
from fastapi import APIRouter
import fastapi.security as _security
from starlette import status
import services as _services, schemas as _schemas
import sqlalchemy.orm as _orm
from providers import hash_provider, token_provider
from .auth_utils import get_usuario_atual

router_autorizacao = APIRouter()


@router_autorizacao.post('/signup',
                         status_code=status.HTTP_201_CREATED,
                         response_model=_schemas.User)
async def signup(usuario: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    if await _services.existe_usuario(usuario.login_ad):
        raise _fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário com este login já cadastrado.")
    return await _services.criar_usuario(usuario, db)


@router_autorizacao.post("/token", response_model = _schemas.LoginSucesso)
async def login(login_data: _schemas.LoginData, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    senha = login_data.senha
    login_ad = login_data.login_ad
    usuario = await _services.get_usuario_by_login(login_ad, db)
    if not usuario:
        raise _fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login e/ou senha inválidos.")
    senha_valida = hash_provider.verificar_hash(senha, usuario.hash_senha)
    if not senha_valida:
        raise _fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login e/ou senha inválidos.")
    token = token_provider.criar_access_token({'sub' : usuario.login_ad})
    result = _schemas.LoginSucesso(login_ad=usuario.login_ad, token=token)
    return result


@router_autorizacao.get('/me', response_model=_schemas.User)
def me(usuario: _schemas.User = _fastapi.Depends(get_usuario_atual)):
    return usuario
