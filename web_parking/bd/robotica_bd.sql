CREATE TABLE robot (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    identificador TEXT UNIQUE,
    ip TEXT,
    estat TEXT, -- "online", "offline"
    ultima_connexio TIMESTAMP
);
