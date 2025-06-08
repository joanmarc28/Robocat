from app.models import Targeta, ClientTargeta
from sqlalchemy.orm import Session

# crea una nova targeta amb numero i tipus especificats i l'afegeix a la base de dades
async def create_targeta(db: Session, num: str, tipus: str):
    nova_targeta = Targeta(num=num, tipus=tipus)
    db.add(nova_targeta)  # afegeix la targeta a la sessio
    db.commit()           # confirma la transaccio
    db.refresh(nova_targeta)  # refresca l'objecte amb la info de la db
    return nova_targeta    # retorna la targeta creada

# obté una targeta segons el seu numero
async def get_targeta(db: Session, num: str):
    return db.query(Targeta).filter(Targeta.num == num).first()  # retorna la targeta o None

# elimina una targeta segons el seu numero
async def delete_targeta(db: Session, num: str):
    targeta = get_targeta(db, num)  # busca la targeta
    if targeta:
        db.delete(targeta)  # elimina la targeta si existeix
        db.commit()         # confirma la eliminacio
    return targeta           # retorna la targeta eliminada o None

# crea lligam entre client i targeta a la taula ClientTargeta
async def link_client_targeta(db: Session, dni_usuari: str, num_targeta: str):
    link = ClientTargeta(dni_usuari=dni_usuari, num_targeta=num_targeta)
    db.add(link)  # afegeix el lligam a la sessio
    db.commit()   # confirma la transaccio
    db.refresh(link)  # refresca l'objecte amb la info de la db
    return link    # retorna el lligam creat
