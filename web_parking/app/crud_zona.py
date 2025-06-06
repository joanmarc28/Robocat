from app.models import Zona
from sqlalchemy.orm import Session

async def create_zona(db: Session, tipus: str, ciutat: str, carrer: str, preu_min: float, temps_maxim: int, coordenades: str):
    nova_zona = Zona(
        tipus=tipus,
        ciutat=ciutat,
        carrer=carrer,
        preu_min=preu_min,
        temps_maxim=temps_maxim,
        coordenades=coordenades
    )
    db.add(nova_zona)
    db.commit()
    db.refresh(nova_zona)
    return nova_zona

async def get_zona(db: Session, zona_id: int):
    return db.query(Zona).filter(Zona.id == zona_id).first()

async def get_all_zones(db: Session):
    return db.query(Zona).all()

async def update_zona(db: Session, zona_id: int, updates: dict):
    zona = get_zona(db, zona_id)
    if not zona:
        return None
    for key, value in updates.items():
        setattr(zona, key, value)
    db.commit()
    db.refresh(zona)
    return zona

async def delete_zona(db: Session, zona_id: int):
    zona = get_zona(db, zona_id)
    if zona:
        db.delete(zona)
        db.commit()
    return zona
