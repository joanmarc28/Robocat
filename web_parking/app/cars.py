from fastapi import APIRouter, Form, Request, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Cotxe, Client
import json
from fastapi.responses import RedirectResponse
from sqlalchemy import select

router = APIRouter()

@router.post("/guardar-cotxe")
async def guardar_cotxe(
    matricula: str = Form(...),
    marca: str = Form(...),
    model: str = Form(...),
    color: str = Form(...),
    any_matriculacio: int = Form(...),
    imatge: str = Form(...),
    dgt: str = Form(...),
    combustible: str = Form(...),
    dni_usuari: str = Form(...), 
    db: Session = Depends(get_db)
):
    #comprova si existeix
    cotxe_existent = db.query(Cotxe).filter(Cotxe.matricula == matricula).first()
    if cotxe_existent:
        raise HTTPException(status_code=400, detail="Aquest cotxe ja existeix")

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

    client = db.query(Client).filter(Client.dni == dni_usuari).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client no trobat")

    client.cotxes.append(nou_cotxe) #afegeix relacio cotxe-client
    db.commit()
    db.refresh(nou_cotxe)

    return {
        "message": "Cotxe guardat correctament i vinculat al client!",
        "cotxe": {
            "matricula": nou_cotxe.matricula,
            "marca": nou_cotxe.marca,
            "model": nou_cotxe.model,
            "color": nou_cotxe.color,
            "any_matriculacio": nou_cotxe.any_matriculacio,
            "imatge": nou_cotxe.imatge,
            "dgt": nou_cotxe.dgt,
            "combustible": nou_cotxe.combustible
        }
    }


@router.get("/obtenir-cotxe")
def obtenir_cotxe(
    matricula: str,
    dni: str,
    db: Session = Depends(get_db)
):
    cotxe = (
        db.query(Cotxe)
        .join(Cotxe.clients)
        .filter(Cotxe.matricula == matricula, Client.dni == dni)
        .first()
    )

    if not cotxe:
        raise HTTPException(status_code=404, detail="Cotxe no trobat per aquest client")

    return {
        "matricula": cotxe.matricula,
        "marca": cotxe.marca,
        "model": cotxe.model,
        "color": cotxe.color,
        "any_matriculacio": cotxe.any_matriculacio,
        "imatge": cotxe.imatge,
        "dgt": cotxe.dgt,
        "combustible": cotxe.combustible
    }


#eliminar cotxe
@router.post("/eliminar-cotxe")
async def eliminar_cotxe(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    matricula = data.get("matricula")

    cotxe = db.query(Cotxe).filter(Cotxe.matricula == matricula).first()
    if cotxe:
        db.delete(cotxe)
        db.commit()
        return {"success": True, "message": f"Cotxe {matricula} eliminat"}
    return {"success": False, "error": "Cotxe no trobat"}
