from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, Boolean,
    DECIMAL, Interval, TIMESTAMP, Table, DateTime
)
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# Taula associativa Possessio (Client ↔ Cotxe)
possessio_table = Table(
    "possessio",
    Base.metadata,
    Column("dni_usuari", String, ForeignKey("client.dni"), primary_key=True),
    Column("matricula_cotxe", String, ForeignKey("cotxe.matricula"), primary_key=True),
)

class Robot(Base):
    __tablename__ = "robot"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    identificador = Column(String, unique=True, index=True)
    ip = Column(String)
    estat = Column(String)  # "online" o "offline"
    ultima_connexio = Column(DateTime, default=datetime.utcnow)


class Usuari(Base):
    __tablename__ = "usuari"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    data_naixement = Column(Date, nullable=False)
    ciutat = Column(String, nullable=False)
    pais = Column(String, nullable=True)
    password = Column(String, nullable=False)

    client = relationship("Client", back_populates="usuari", uselist=False)
    policia = relationship("Policia", back_populates="usuari", uselist=False)


class Client(Base):
    __tablename__ = "client"
    dni = Column(String, primary_key=True, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("usuari.id", ondelete="CASCADE"), nullable=False)
    nom = Column(String, nullable=False)
    cognoms = Column(String, nullable=True)
    direccio = Column(String, nullable=True)
    codi_postal = Column(String, nullable=True)
    telefon = Column(String, nullable=True)

    usuari = relationship("Usuari", back_populates="client")
    cotxes = relationship("Cotxe", secondary=possessio_table, back_populates="clients")
    targetes = relationship("ClientTargeta", back_populates="client")
    estades = relationship("Estada", back_populates="client")


class Policia(Base):
    __tablename__ = "policia"
    user_id = Column(Integer, ForeignKey("usuari.id", ondelete="CASCADE"), primary_key=True)
    placa = Column(String, unique=True, nullable=False)

    usuari = relationship("Usuari", back_populates="policia")


class Cotxe(Base):
    __tablename__ = "cotxe"
    matricula = Column(String, primary_key=True)
    marca = Column(String)
    model = Column(String)
    color = Column(String)
    any_matriculacio = Column(Integer)
    imatge = Column(String)
    dgt = Column(String)
    combustible = Column(String)

    clients = relationship("Client", secondary=possessio_table, back_populates="cotxes")
    estades = relationship("Estada", back_populates="cotxe")


class Targeta(Base):
    __tablename__ = "targeta"
    num = Column(String, primary_key=True)
    tipus = Column(String)

    clients = relationship("ClientTargeta", back_populates="targeta")


class ClientTargeta(Base):
    __tablename__ = "client_targeta"
    dni_usuari = Column(String, ForeignKey("client.dni"), primary_key=True)
    num_targeta = Column(String, ForeignKey("targeta.num"), primary_key=True)

    client = relationship("Client", back_populates="targetes")
    targeta = relationship("Targeta", back_populates="clients")


class Zona(Base):
    __tablename__ = "zona"
    id = Column(Integer, primary_key=True, index=True)
    tipus = Column(String)
    ciutat = Column(String)
    carrer = Column(String)
    preu_min = Column(DECIMAL)
    temps_maxim = Column(Integer)
    coordenades = Column(String)

    estades = relationship("Estada", back_populates="zona")


class Estada(Base):
    __tablename__ = "estada"
    id = Column(Integer, primary_key=True, index=True)
    dni_usuari = Column(String, ForeignKey("client.dni"))
    matricula_cotxe = Column(String, ForeignKey("cotxe.matricula"))
    id_zona = Column(Integer, ForeignKey("zona.id"))
    data_inici = Column(TIMESTAMP)
    data_final = Column(TIMESTAMP)
    durada = Column(Interval)
    preu = Column(DECIMAL)
    activa = Column(Boolean)

    client = relationship("Client", back_populates="estades")
    cotxe = relationship("Cotxe", back_populates="estades")
    zona = relationship("Zona", back_populates="estades")
