-- Agregar columna delivery_options a la tabla businesses
ALTER TABLE businesses 
ADD COLUMN delivery_options TEXT NULL COMMENT 'Opciones de entrega del negocio (JSON o texto)';