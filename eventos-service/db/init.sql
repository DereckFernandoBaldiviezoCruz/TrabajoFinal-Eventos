-- db/init.sql

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS eventos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL,
    deporte VARCHAR(100) NOT NULL,          -- fútbol, tenis, etc.
    fecha TIMESTAMP WITH TIME ZONE NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'programado', -- programado, en_curso, finalizado, cancelado
    equipo_local VARCHAR(255),
    equipo_visitante VARCHAR(255),
    cuota_local DECIMAL(5, 2),
    cuota_empate DECIMAL(5, 2),
    cuota_visitante DECIMAL(5, 2),
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
