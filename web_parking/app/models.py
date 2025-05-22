from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Usuari(Base):
    __tablename__ = "usuari"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    data_naixement = Column(Date, nullable=False)
    ciutat = Column(String, nullable=False)
    password = Column(String, nullable=False)

    client = relationship("Client", back_populates="usuari", uselist=False)
    policia = relationship("Policia", back_populates="usuari", uselist=False)


class Client(Base):
    __tablename__ = "client"
    user_id = Column(Integer, ForeignKey("usuari.id", ondelete="CASCADE"), primary_key=True)
    dni = Column(String, unique=True, nullable=False)
    nom = Column(String, nullable=False)
    cognoms = Column(String)
    direccio = Column(String)
    codi_postal = Column(String)
    telefon = Column(String)

    usuari = relationship("Usuari", back_populates="client")


class Policia(Base):
    __tablename__ = "policia"
    user_id = Column(Integer, ForeignKey("usuari.id", ondelete="CASCADE"), primary_key=True)
    placa = Column(String, unique=True, nullable=False)

    usuari = relationship("Usuari", back_populates="policia")