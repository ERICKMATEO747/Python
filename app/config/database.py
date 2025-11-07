import pymysql
from app.config.settings import settings
from app.utils.logger import log_info

def get_db_connection():
    """Obtiene conexión a la base de datos MySQL"""
    try:
        # Parsear URL de conexión
        url_parts = settings.database_url.replace("mysql+pymysql://", "").split("/")
        auth_db = url_parts[1]
        host_port_user = url_parts[0].split("@")
        host_port = host_port_user[1].split(":")
        user_pass = host_port_user[0].split(":")
        
        connection = pymysql.connect(
            host=host_port[0],
            port=int(host_port[1]),
            user=user_pass[0],
            password=user_pass[1],
            database=auth_db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        raise Exception(f"Error conectando a la base de datos: {str(e)}")

def init_database():
    """Inicializa la base de datos y crea las tablas si no existen"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Tabla users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NULL,
                    telefono VARCHAR(20) UNIQUE NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT chk_contact CHECK (email IS NOT NULL OR telefono IS NOT NULL)
                )
            """)
            
            # Tabla otp_codes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS otp_codes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(100) NOT NULL,
                    otp_code VARCHAR(6) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_email_otp (email, otp_code),
                    INDEX idx_expires (expires_at)
                )
            """)
            
            # Tabla user_types
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_types (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    type_name VARCHAR(50) NOT NULL UNIQUE,
                    type_hash VARCHAR(64) NOT NULL UNIQUE,
                    description VARCHAR(200),
                    active TINYINT(1) DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insertar tipos de usuario por defecto solo si no existen
            cursor.execute("SELECT COUNT(*) as count FROM user_types")
            user_types_count = cursor.fetchone()['count']
            
            if user_types_count == 0:
                cursor.execute("""
                    INSERT INTO user_types (type_name, type_hash, description) VALUES 
                    ('cliente', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', 'Usuario cliente final'),
                    ('negocio', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1', 'Usuario propietario de negocio'),
                    ('admin', 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1b2', 'Administrador del sistema')
                """)
                log_info("Tipos de usuario insertados")
            else:
                log_info("Tipos de usuario ya existen, omitiendo inserción")
            
            # Tabla municipalities
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS municipalities (
                    id BIGINT PRIMARY KEY AUTO_INCREMENT,
                    municipio VARCHAR(100) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla businesses
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS businesses (
                    id BIGINT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(200) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    address TEXT,
                    municipality_id BIGINT,
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    logo VARCHAR(500),
                    description TEXT,
                    rating DECIMAL(2,1) DEFAULT 0.0,
                    facebook VARCHAR(500),
                    instagram VARCHAR(500),
                    tiktok VARCHAR(500),
                    whatsapp VARCHAR(500),
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (municipality_id) REFERENCES municipalities(id)
                )
            """)
            
            # Agregar índice único para evitar duplicados en businesses
            try:
                cursor.execute("ALTER TABLE businesses ADD UNIQUE INDEX idx_business_name (name)")
                log_info("Índice único agregado a businesses.name")
            except Exception as e:
                if "Duplicate key name" not in str(e):
                    log_info(f"No se pudo agregar índice único: {str(e)}")
            
            # Tabla business_menu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS business_menu (
                    id BIGINT PRIMARY KEY AUTO_INCREMENT,
                    business_id BIGINT NOT NULL,
                    producto VARCHAR(200) NOT NULL,
                    descripcion TEXT,
                    precio DECIMAL(10,2) NOT NULL,
                    categoria VARCHAR(100),
                    disponible BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (business_id) REFERENCES businesses(id)
                )
            """)
            
            # Tabla user_visits (sin foreign keys inicialmente)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_visits (
                    id BIGINT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    business_id BIGINT NOT NULL,
                    visit_date TIMESTAMP NOT NULL,
                    visit_month VARCHAR(7) NOT NULL,
                    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'completed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_user_business_month (user_id, business_id, visit_month)
                )
            """)
            
            # Agregar foreign keys después si no existen
            try:
                cursor.execute("""
                    SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'user_visits' 
                    AND COLUMN_NAME = 'user_id' 
                    AND REFERENCED_TABLE_NAME = 'users'
                """)
                fk_user_exists = cursor.fetchone()['count'] > 0
                
                if not fk_user_exists:
                    cursor.execute("ALTER TABLE user_visits ADD FOREIGN KEY (user_id) REFERENCES users(id)")
                    log_info("Foreign key user_id en user_visits agregada")
            except Exception as e:
                log_info(f"No se pudo agregar FK user_id: {str(e)}")
            
            try:
                cursor.execute("""
                    SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'user_visits' 
                    AND COLUMN_NAME = 'business_id' 
                    AND REFERENCED_TABLE_NAME = 'businesses'
                """)
                fk_business_exists = cursor.fetchone()['count'] > 0
                
                if not fk_business_exists:
                    cursor.execute("ALTER TABLE user_visits ADD FOREIGN KEY (business_id) REFERENCES businesses(id)")
                    log_info("Foreign key business_id en user_visits agregada")
            except Exception as e:
                log_info(f"No se pudo agregar FK business_id: {str(e)}")
            
            # Verificar y agregar columnas a users si no existen
            columns_to_add = [
                ('user_type_id', 'INT NOT NULL DEFAULT 1'),
                ('municipality_id', 'BIGINT'),
                ('avatar', 'VARCHAR(500)')
            ]
            
            for column_name, column_def in columns_to_add:
                cursor.execute("""
                    SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'users' 
                    AND COLUMN_NAME = %s
                """, (column_name,))
                column_exists = cursor.fetchone()['count'] > 0
                
                if not column_exists:
                    log_info(f"Agregando columna {column_name} a tabla users")
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_def}")
            
            # Agregar foreign keys si no existen
            fks_to_add = [
                ('user_type_id', 'user_types'),
                ('municipality_id', 'municipalities')
            ]
            
            for column_name, ref_table in fks_to_add:
                cursor.execute("""
                    SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'users' 
                    AND COLUMN_NAME = %s 
                    AND REFERENCED_TABLE_NAME = %s
                """, (column_name, ref_table))
                fk_exists = cursor.fetchone()['count'] > 0
                
                if not fk_exists:
                    cursor.execute(f"ALTER TABLE users ADD FOREIGN KEY ({column_name}) REFERENCES {ref_table}(id)")
                    log_info(f"Foreign key {column_name} agregada exitosamente")
            
            # Insertar datos de prueba solo si no existen
            try:
                # Verificar si ya existen municipios
                cursor.execute("SELECT COUNT(*) as count FROM municipalities")
                municipality_count = cursor.fetchone()['count']
                
                if municipality_count == 0:
                    cursor.execute("""
                        INSERT INTO municipalities (municipio, state) VALUES
                        ('Papantla', 'Veracruz'),
                        ('Coatzintla', 'Veracruz'),
                        ('Poza Rica', 'Veracruz'),
                        ('Tuxpan', 'Veracruz')
                    """)
                    log_info("Municipios de ejemplo insertados")
                else:
                    log_info("Municipios ya existen, omitiendo inserción")
                
                # Verificar si ya existen businesses
                cursor.execute("SELECT COUNT(*) as count FROM businesses")
                business_count = cursor.fetchone()['count']
                
                if business_count == 0:
                    cursor.execute("""
                        INSERT INTO businesses (name, category, address, municipality_id, phone, email, description, rating, facebook, instagram, tiktok, whatsapp) VALUES
                        ('Restaurante El Totonaco', 'Restaurante', 'Calle Enríquez 123, Centro', 1, '7841234567', 'contacto@eltotonaco.com', 'Comida tradicional veracruzana', 4.5, 'https://facebook.com/eltotonaco', 'https://instagram.com/eltotonaco', 'https://tiktok.com/@eltotonaco', 'https://wa.me/527841234567'),
                        ('Café Vanilla', 'Cafetería', 'Av. 20 de Noviembre 45', 2, '7822345678', 'info@cafevanilla.com', 'Café de especialidad y vainilla', 4.2, 'https://facebook.com/cafevanilla', 'https://instagram.com/cafevanilla', 'https://tiktok.com/@cafevanilla', 'https://wa.me/527822345678'),
                        ('Boutique Jarocha', 'Ropa', 'Plaza Poza Rica 67', 3, '7823456789', 'ventas@boutiquejarocha.com', 'Ropa y accesorios regionales', 4.0, 'https://facebook.com/boutiquejarocha', 'https://instagram.com/boutiquejarocha', 'https://tiktok.com/@boutiquejarocha', 'https://wa.me/527823456789'),
                        ('Farmacia del Puerto', 'Farmacia', 'Malecón Tuxpan 89', 4, '7834567890', 'contacto@farmaciapuerto.com', 'Medicamentos y productos de salud', 4.3, 'https://facebook.com/farmaciapuerto', 'https://instagram.com/farmaciapuerto', 'https://tiktok.com/@farmaciapuerto', 'https://wa.me/527834567890'),
                        ('Gimnasio Coatza Fit', 'Deportes', 'Calle Hidalgo 12', 2, '7825678901', 'info@coatzafit.com', 'Gimnasio y entrenamiento personal', 4.4, 'https://facebook.com/coatzafit', 'https://instagram.com/coatzafit', 'https://tiktok.com/@coatzafit', 'https://wa.me/527825678901')
                    """)
                    log_info("Businesses de ejemplo insertados")
                else:
                    log_info("Businesses ya existen, omitiendo inserción")
                
                # Insertar menús de ejemplo solo si no existen
                cursor.execute("SELECT COUNT(*) as count FROM business_menu")
                menu_count = cursor.fetchone()['count']
                
                if menu_count == 0:
                    cursor.execute("""
                        INSERT INTO business_menu (business_id, producto, descripcion, precio, categoria) VALUES
                        (1, 'Mole de Olla', 'Mole tradicional veracruzano con pollo', 85.00, 'Platillos'),
                        (1, 'Pescado a la Veracruzana', 'Pescado fresco con salsa veracruzana', 120.00, 'Platillos'),
                        (1, 'Agua de Chía con Limón', 'Bebida refrescante natural', 30.00, 'Bebidas'),
                        (2, 'Café de Olla', 'Café tradicional con canela y piloncillo', 45.00, 'Cafés'),
                        (2, 'Flan de Vainilla', 'Postre con vainilla de Papantla', 55.00, 'Postres'),
                        (2, 'Torta de Jamón', 'Torta veracruzana con ingredientes frescos', 65.00, 'Alimentos'),
                        (3, 'Guayabera Bordada', 'Guayabera tradicional veracruzana', 450.00, 'Ropa'),
                        (3, 'Huipil Totonaco', 'Huipil artesanal de la región', 650.00, 'Ropa'),
                        (3, 'Huaraches de Cuero', 'Calzado artesanal mexicano', 380.00, 'Calzado'),
                        (4, 'Paracetamol 500mg', 'Analgésico y antipirético', 25.00, 'Medicamentos'),
                        (4, 'Vitamina C', 'Suplemento vitamínico 1000mg', 180.00, 'Suplementos'),
                        (4, 'Termómetro Digital', 'Termómetro clínico digital', 120.00, 'Equipos'),
                        (5, 'Membresía Mensual', 'Acceso completo al gimnasio por 1 mes', 350.00, 'Membresías'),
                        (5, 'Clase de Zumba', 'Clase grupal de baile y ejercicio', 60.00, 'Clases'),
                        (5, 'Entrenamiento Personal', 'Sesión individual con entrenador', 250.00, 'Servicios')
                    """)
                    log_info("Menús de ejemplo insertados")
                else:
                    log_info("Menús ya existen, omitiendo inserción")
                log_info("Datos de prueba verificados correctamente")
            except Exception as e:
                log_info(f"Error insertando datos de prueba: {str(e)}")
            
            connection.commit()
            log_info("Base de datos inicializada correctamente")
    except Exception as e:
        log_error("Error inicializando base de datos", error=e)
        raise
    finally:
        connection.close()