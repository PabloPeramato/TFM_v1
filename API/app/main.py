from fastapi import FastAPI, HTTPException, Depends
from app.api.routers import sessions, availability, user, power
from app.core.config import settings
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html

security = HTTPBasic()

USERNAME = settings.USERNAME_SWAGGER
PASSWORD = settings.PASSWORD_SWAGGER


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return credentials


app = FastAPI(
    title="API de Gestión de Raspberry Pi",
    description=(
        "Esta API permite gestionar las sesiones y la disponibilidad "
        "de dispositivos Raspberry Pi."),
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)
app.include_router(
    sessions.router,
    prefix="/sessions",
    tags=["sessions"]
)
app.include_router(
    availability.router,
    prefix="/availability",
    tags=["availability"]
)
app.include_router(
    user.router,
    prefix="/users",
    tags=["users"]
)
app.include_router(
    power.router,
    prefix="/power",
    tags=["power"]
)


@app.get("/docs", include_in_schema=False)
def get_documentation(
        credentials: HTTPBasicCredentials = Depends(authenticate)
        ):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")
