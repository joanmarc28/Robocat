from fastapi import APIRouter, Request, Form, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud_users import create_user
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="app/templates")

@router.post("/registre")
async def processar_registre(
    email: str = Form(...),
    password: str = Form(...),
    data_naixement: str = Form(...),
    ciutat: str = Form(...),
    es_policia: bool = Form(False),
    dni: str = Form(None),
    nom: str = Form(None),
    cognoms: str = Form(None),
    direccio: str = Form(None),
    codi_postal: str = Form(None),
    telefon: str = Form(None),
    placa: str = Form(None),
    db: Session = Depends(get_db)
):
    await create_user(
        db=db,
        email=email,
        password=pwd_context.hash(password),
        data_naixement=data_naixement,
        ciutat=ciutat,
        es_policia=es_policia,
        dni=dni,
        nom=nom,
        cognoms=cognoms,
        direccio=direccio,
        codi_postal=codi_postal,
        telefon=telefon,
        placa=placa
    )
    return RedirectResponse(url="/login", status_code=303)



@router.get("/login")
def parking(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request
    })

@router.get("/registre")
def parking(request: Request):
    return templates.TemplateResponse("registre.html", {
        "request": request
    })