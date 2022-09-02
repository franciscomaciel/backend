import fastapi as _fastapi
from fastapi import APIRouter
import fastapi.security as _security
from starlette import status
import services as _services, schemas as _schemas
import sqlalchemy.orm as _orm
from providers import hash_provider

router_autorizacao = APIRouter()


@router_autorizacao.post('/signup',
                         status_code=status.HTTP_201_CREATED,
                         response_model=_schemas.User)
async def signup(usuario: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    if await _services.existe_usuario(usuario.login):
        raise _fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário com este login já cadastrado.")
    return await _services.criar_usuario(usuario, db)


@router_autorizacao.post("/token", status_code=status.HTTP_200_OK)
                         # ,response_model=_schemas.LoginSucesso)
async def login(login_data: _schemas.LoginData, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    senha = login_data.senha
    login = login_data.login
    usuario = await _services.get_usuario_by_login(login, db)
    if not usuario:
        raise _fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login e/ou senha inválidos.")
    senha_valida = hash_provider.verificar_hash(senha, usuario.hash_senha)
    if not senha_valida:
        raise _fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login e/ou senha inválidos.")
    return usuario


@router_autorizacao.get("/users/me", response_model=_schemas.User)
async def get_usuario_conectado(usuario:_schemas.User = _fastapi.Depends(_services.get_usuario_atual)):
    return usuario