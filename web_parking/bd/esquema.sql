-- Taula Usuari
CREATE TABLE Usuari (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    data_naixement DATE NOT NULL,
    Ciutat TEXT NOT NULL,
    Pais TEXT
);

-- Taula Policia
CREATE TABLE Policia (
    user_id INTEGER PRIMARY KEY REFERENCES Usuari(id),
    Placa TEXT NOT NULL
);

-- Taula Client
CREATE TABLE Client (
    DNI TEXT PRIMARY KEY,
    user_id INTEGER REFERENCES Usuari(id),
    Nom TEXT,
    Cognoms TEXT,
    codi_postal TEXT,
    direccio TEXT,
    Credits INTEGER DEFAULT 0,
    Telefon numeric(15),
);

-- Taula Cotxe
CREATE TABLE Cotxe (
    Matricula TEXT PRIMARY KEY,
    Marca TEXT,
    Model TEXT,
    Color TEXT,
    any_matriculacio INTEGER,
    Imatge TEXT,
    DGT TEXT,
    Combustible TEXT
);

-- Taula relació Usuari-Cotxe (Possessió)
CREATE TABLE Possessio (
    DNI_Usuari TEXT REFERENCES Client(DNI),
    Matricula_Cotxe TEXT REFERENCES Cotxe(Matricula),
    PRIMARY KEY (DNI_Usuari, Matricula_Cotxe)
);

-- Taula Targeta
CREATE TABLE Targeta (
    Num TEXT PRIMARY KEY,
    Tipus TEXT
);

-- Taula relació Client-Targeta
CREATE TABLE Client_Targeta (
    DNI_Usuari TEXT REFERENCES Client(DNI),
    Num_Targeta TEXT REFERENCES Targeta(Num),
    PRIMARY KEY (DNI_Usuari, Num_Targeta)
);

-- Taula Zona
CREATE TABLE Zona (
    id SERIAL PRIMARY KEY,
    Tipus TEXT,
    Ciutat TEXT,
    Carrer TEXT,
    Preu_Min DECIMAL,
    Temps_Maxim INTEGER,
    Coordenades TEXT
);

-- Taula Estada
CREATE TABLE Estada (
    id SERIAL PRIMARY KEY,
    DNI_Usuari TEXT REFERENCES Client(DNI),
    Matricula_Cotxe TEXT REFERENCES Cotxe(Matricula),
    id_Zona INTEGER REFERENCES Zona(id),
    Data_Inici TIMESTAMP ,
    Data_Final TIMESTAMP ,
    Durada INTERVAL,
    Preu DECIMAL,
    Activa BOOLEAN
);
