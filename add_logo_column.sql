-- Agregar columna logo_url a la tabla businesses
ALTER TABLE businesses 
ADD COLUMN logo_url TEXT NULL COMMENT 'URL del logo del negocio';