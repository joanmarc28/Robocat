from app.models import Targeta, ClientTargeta
from sqlalchemy.orm import Session

async def create_targeta(db: Session, num: str, tipus: str):
    nova_targeta = Targeta(num=num, tipus=tipus)
    db.add(nova_targeta)
    db.commit()
    db.refresh(nova_targeta)
    return nova_targeta

async def get_targeta(db: Session, num: str):
    return db.query(Targeta).filter(Targeta.num == num).first()

async def delete_targeta(db: Session, num: str):
    targeta = get_targeta(db, num)
    if targeta:
        db.delete(targeta)
        db.commit()
    return targeta

async def link_client_targeta(db: Session, dni_usuari: str, num_targeta: str):
    link = ClientTargeta(dni_usuari=dni_usuari, num_targeta=num_targeta)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link
