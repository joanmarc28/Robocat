from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import sys

# 🔥 Afegeix manualment el path del projecte al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.database import engine, SessionLocal
from app.models import Estada


def actualitzar_estades():
    db = SessionLocal()
    try:
        ara = datetime.utcnow()
        estades = db.query(Estada).filter(Estada.activa == True).all()
        for estada in estades:
            if estada.data_final and estada.data_final <= ara:
                print(f"[{ara}] Estada {estada.id} expirada, desactivant.")
                estada.activa = False
            else:
                temps_restant = estada.data_final - ara if estada.data_final else None
                print(f"[{ara}] Estada {estada.id} encara activa. Temps restant: {temps_restant}")
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    actualitzar_estades()

