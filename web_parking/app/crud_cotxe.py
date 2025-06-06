from app.models import Cotxe, Client
from sqlalchemy.orm import Session

async def create_cotxe(
    db: Session,
    matricula: str,
    marca: str,
    model: str,
    color: str,
    any_matriculacio: int,
    imatge: str,
    dgt: str,
    combustible: str
):
    nou_cotxe = Cotxe(
        matricula=matricula,
        marca=marca,
        model=model,
        color=color,
        any_matriculacio=any_matriculacio,
        imatge=imatge,
        dgt=dgt,
        combustible=combustible
    )
    db.add(nou_cotxe)
    db.commit()
    db.refresh(nou_cotxe)
    return nou_cotxe

async def delete_cotxe(db: Session, matricula: str):
    cotxe = db.query(Cotxe).filter(Cotxe.matricula == matricula).first()
    if cotxe:
        db.delete(cotxe)
        db.commit()
    return cotxe

async def update_cotxe(
    db: Session,
    matricula: str,
    marca: str = None,
    model: str = None,
    color: str = None,
    any_matriculacio: int = None,
    imatge: str = None,
    dgt: str = None,
    combustible: str = None
):
    cotxe = db.query(Cotxe).filter(Cotxe.matricula == matricula).first()
    if not cotxe:
        return None

    if marca is not None:
        cotxe.marca = marca
    if model is not None:
        cotxe.model = model
    if color is not None:
        cotxe.color = color
    if any_matriculacio is not None:
        cotxe.any_matriculacio = any_matriculacio
    if imatge is not None:
        cotxe.imatge = imatge
    if dgt is not None:
        cotxe.dgt = dgt
    if combustible is not None:
        cotxe.combustible = combustible

    db.commit()
    db.refresh(cotxe)
    return cotxe

async def get_cotxe(db: Session, matricula: str):
    return db.query(Cotxe).filter(Cotxe.matricula == matricula).first()

async def get_cotxes_by_client(db: Session, dni_usuari: str):
    client = db.query(Client).filter(Client.dni == dni_usuari).first()
    if not client:
        return None
    return client.cotxes
