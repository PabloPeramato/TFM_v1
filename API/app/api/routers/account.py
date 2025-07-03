from fastapi import APIRouter, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from app.models.schemas import Token, User as DBUser
from app.core.database import SessionLocal
from app.core.config import settings

router = APIRouter()

FAKE_USERS_DB = settings.FAKE_USERS_DB
PASSWORD_PXE = settings.PASSWORD_PXE
ALGORITHM = settings.ALGORITHM

# Seguridad y contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")

db = SessionLocal()


# Funciones auxiliares
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, PASSWORD_PXE, algorithm=ALGORITHM)


# Endpoints
@router.post("/register", response_model=Token, tags=["account"])
def register(
        mail: EmailStr = Query(
            ...,
            description="Correo electrónico del usuario"
        ),
        username: str = Query(
            ...,
            description="Nombre de usuario"
        ),
        password: str = Query(
            ...,
            description="Contraseña"
        ),
        confirm_password: str = Query(
            ...,
            description="Confirmación de contraseña"
        ),
        ):

    user_exists = db.query(DBUser).filter(DBUser.username == username).first()
    mail_exists = db.query(DBUser).filter(DBUser.email == mail).first()

    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe."
        )
    if mail_exists:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está registrado."
        )
    if username in FAKE_USERS_DB:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario es inválido."
        )
    if password != confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Las contraseñas no coinciden."
        )

    hashed_pw = get_password_hash(password)
    db_user = DBUser(
        email=mail,
        username=username,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token, tags=["account"])
def login(
        login_field: str = Query(
            ...,
            description="Correo electrónico o nombre de usuario"
        ),
        password: str = Query(
            ...,
            description="Contraseña"
        ),
        ):

    user = db.query(DBUser).filter(
        (DBUser.username == login_field) | (DBUser.email == login_field)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
