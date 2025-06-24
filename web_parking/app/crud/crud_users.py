from app.models import Usuari, Client, Policia
from sqlalchemy.orm import Session
from datetime import datetime

# crea un usuari nou amb les dades proporcionades i el guarda a la base de dades
async def create_user(
    db: Session,
    email: str,
    password: str,
    data_naixement: str,
    ciutat: str,
    pais: str,
    es_policia: bool,
    dni: str = None,
    nom: str = None,
    cognoms: str = None,
    direccio: str = None,
    codi_postal: str = None,
    telefon: str = None,
    placa: str = None
):
    data_naixement_dt = datetime.strptime(data_naixement, "%Y-%m-%d").date()  # converteix la data a objecte date
    nou_usuari = Usuari(
        email=email,
        password=password,
        data_naixement=data_naixement_dt,
        ciutat=ciutat
    )
    db.add(nou_usuari)  # afegeix l'usuari a la sessio
    db.commit()         # confirma la transaccio
    db.refresh(nou_usuari)  # refresca l'objecte amb la info de la db

    if es_policia:
        nou_policia = Policia(
            user_id=nou_usuari.id,
            placa=placa
        )
        db.add(nou_policia)  # afegeix el policia si es poliica
    else:
        nou_client = Client(
            user_id=nou_usuari.id,
            dni=dni,
            nom=nom,
            cognoms=cognoms,
            direccio=direccio,
            codi_postal=codi_postal,
            telefon=telefon
        )
        db.add(nou_client)  # afegeix el client si no es policia

    db.commit()  # confirma la transaccio per policia o client
    return nou_usuari  # retorna l'usuari creat
