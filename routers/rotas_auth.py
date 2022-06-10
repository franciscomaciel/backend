import fastapi as _fastapi
from fastapi import APIRouter
import fastapi.security as _security
from starlette import status
import services as _services, schemas as _schemas
import sqlalchemy.orm as _orm

router_autorizacao = APIRouter()


@router_autorizacao.post('/signup',
                         status_code=status.HTTP_201_CREATED,
                         response_model=_schemas.User)
async def signup(usuario: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    if await _services.existe_usuario(usuario.login_ad):
        raise _fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login do AD já cadastrado.")
    return await _services.criar_usuario(usuario, db)


@router_autorizacao.post("/token", status_code=status.HTTP_200_OK)
                         # ,response_model=_schemas.LoginSucesso)
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    usuario = await _services.autenticar_usuario(form_data.username, form_data.password, db)

    if not usuario:
        raise _fastapi.HTTPException(status_code=401, detail="Login do AD ou senha inválida.")

    return await _services.criar_token(usuario)


@router_autorizacao.get("/users/me", response_model=_schemas.User)
async def get_usuario_conectado(usuario:_schemas.User = _fastapi.Depends(_services.get_usuario_atual)):
    return usuario