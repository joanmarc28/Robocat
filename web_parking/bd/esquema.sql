-- =========================
-- Esquema Robocat Web Parking (PostgreSQL)
-- ORDENAT per dependències i amb sintaxi corregida
-- =========================

-- Taula Usuari
CREATE TABLE IF NOT EXISTS "Usuari" (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    "Password" TEXT NOT NULL,
    data_naixement DATE NOT NULL,
    "Ciutat" TEXT NOT NULL,
    "Pais" TEXT
);

-- Taula Policia (depèn d'Usuari)
CREATE TABLE IF NOT EXISTS "Policia" (
    user_id INTEGER PRIMARY KEY REFERENCES "Usuari"(id) ON DELETE CASCADE,
    "Placa" TEXT NOT NULL
);

-- Taula Client (depèn d'Usuari)  << CORREGIT: sense coma final
CREATE TABLE IF NOT EXISTS "Client" (
    "DNI" TEXT PRIMARY KEY,
    user_id INTEGER REFERENCES "Usuari"(id) ON DELETE SET NULL,
    "Nom" TEXT,
    "Cognoms" TEXT,
    codi_postal TEXT,
    direccio TEXT,
    "Credits" INTEGER DEFAULT 0,
    "Telefon" NUMERIC(15)
);

-- Taula Cotxe (independent)
CREATE TABLE IF NOT EXISTS "Cotxe" (
    "Matricula" TEXT PRIMARY KEY,
    "Marca" TEXT,
    "Model" TEXT,
    "Color" TEXT,
    any_matriculacio INTEGER,
    "Imatge" TEXT,
    "DGT" TEXT,
    "Combustible" TEXT
);

-- Taula Zona (independent)
CREATE TABLE IF NOT EXISTS "Zona" (
    id SERIAL PRIMARY KEY,
    "Tipus" TEXT,
    "Ciutat" TEXT,
    "Carrer" TEXT,
    "Preu_Min" DECIMAL(10,2),
    "Temps_Maxim" INTEGER,
    "Coordenades" TEXT
);

-- Taula Ruta (depèn de Policia i Zona)
CREATE TABLE IF NOT EXISTS "Ruta" (
    id SERIAL PRIMARY KEY,
    id_policia INTEGER REFERENCES "Policia"(user_id) ON DELETE SET NULL,
    id_zona INTEGER REFERENCES "Zona"(id) ON DELETE SET NULL,
    data_creacio TIMESTAMP NOT NULL,
    origen TEXT NOT NULL,
    desti TEXT NOT NULL
);

-- Taula PuntRuta (depèn de Ruta)
CREATE TABLE IF NOT EXISTS "PuntRuta" (
    id SERIAL PRIMARY KEY,
    id_Ruta INTEGER REFERENCES "Ruta"(id) ON DELETE CASCADE,
    latitud DECIMAL(9,6) NOT NULL,
    longitud DECIMAL(9,6) NOT NULL,
    ordre INTEGER NOT NULL
);

-- Taula Robot (depèn de Ruta)  << MOVUDA després de Ruta
CREATE TABLE IF NOT EXISTS "robot" (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    identificador TEXT UNIQUE,
    ip TEXT,
    estat TEXT, -- "online", "offline"
    id_ruta INTEGER REFERENCES "Ruta"(id) ON DELETE SET NULL,
    ultima_connexio TIMESTAMP
);

-- Taula RoboCatRuta (depèn de robot i Ruta)
CREATE TABLE IF NOT EXISTS "RoboCatRuta" (
    id SERIAL PRIMARY KEY,
    id_RoboCat INTEGER REFERENCES "robot"(id) ON DELETE CASCADE,
    id_Ruta INTEGER REFERENCES "Ruta"(id) ON DELETE CASCADE,
    data_inici TIMESTAMP,
    data_fi TIMESTAMP
);

-- Taula Possessio (relació Client-Cotxe)
CREATE TABLE IF NOT EXISTS "Possessio" (
    DNI_Usuari TEXT REFERENCES "Client"("DNI") ON DELETE CASCADE,
    Matricula_Cotxe TEXT REFERENCES "Cotxe"("Matricula") ON DELETE CASCADE,
    PRIMARY KEY (DNI_Usuari, Matricula_Cotxe)
);

-- Taula Estada (depèn de Client, Cotxe, Zona)
CREATE TABLE IF NOT EXISTS "Estada" (
    id SERIAL PRIMARY KEY,
    DNI_Usuari TEXT REFERENCES "Client"("DNI") ON DELETE SET NULL,
    Matricula_Cotxe TEXT REFERENCES "Cotxe"("Matricula") ON DELETE SET NULL,
    id_Zona INTEGER REFERENCES "Zona"(id) ON DELETE SET NULL,
    Data_Inici TIMESTAMP,
    Data_Final TIMESTAMP,
    Durada INTERVAL,
    Preu DECIMAL(10,2),
    Activa BOOLEAN
);

-- Taula Infraccio (depèn de Client, Cotxe, Zona)
CREATE TABLE IF NOT EXISTS "Infraccio" (
    id SERIAL PRIMARY KEY,
    DNI_Usuari TEXT REFERENCES "Client"("DNI") ON DELETE SET NULL,
    Matricula_Cotxe TEXT REFERENCES "Cotxe"("Matricula") ON DELETE SET NULL,
    id_Zona INTEGER REFERENCES "Zona"(id) ON DELETE SET NULL,
    Data_Infraccio TIMESTAMP,
    Descripcio TEXT,
    Preu DECIMAL(10,2),
    Imatge TEXT
);

-- Taula PossibleInfraccio (depèn de Cotxe)  << CORREGIT: sense caràcters rars i nom net
CREATE TABLE IF NOT EXISTS "PossibleInfraccio" (
    id VARCHAR(255) PRIMARY KEY,
    Descripcio TEXT,
    Matricula_Cotxe TEXT REFERENCES "Cotxe"("Matricula") ON DELETE SET NULL,
    data_posInfraccio TIMESTAMP,
    Imatge TEXT
);
