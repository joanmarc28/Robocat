from app.models import Estada
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

async def create_estada(
    db: Session,
    dni_usuari: str,
    matricula_cotxe: str,
    id_zona: int,
    data_inici: datetime,
    data_final: datetime,
    durada: timedelta,
    preu: float,
    activa: bool
):
    nova_estada = Estada(
        dni_usuari=dni_usuari,
        matricula_cotxe=matricula_cotxe,
        id_zona=id_zona,
        data_inici=data_inici,
        data_final=data_final,
        durada=durada,
        preu=preu,
        activa=activa
    )
    db.add(nova_estada)
    db.commit()
    db.refresh(nova_estada)
    return nova_estada

async def get_estada(db: Session, estada_id: int):
    return db.query(Estada).filter(Estada.id == estada_id).first()

async def get_estades_by_client(db: Session, dni_usuari: str):
    return db.query(Estada).filter(Estada.dni_usuari == dni_usuari).all()

async def update_estada(db: Session, estada_id: int, updates: dict):
    estada = get_estada(db, estada_id)
    if not estada:
        return None
    for key, value in updates.items():
        setattr(estada, key, value)
    db.commit()
    db.refresh(estada)
    return estada

async def delete_estada(db: Session, estada_id: int):
    estada = get_estada(db, estada_id)
    if estada:
        db.delete(estada)
        db.commit()
    return estada
