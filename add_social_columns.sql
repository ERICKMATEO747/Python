-- Agregar columnas de redes sociales a la tabla businesses
ALTER TABLE businesses 
ADD COLUMN website VARCHAR(200) NULL,
ADD COLUMN facebook VARCHAR(200) NULL,
ADD COLUMN instagram VARCHAR(200) NULL,
ADD COLUMN whatsapp VARCHAR(20) NULL;