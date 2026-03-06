import psycopg2
import psycopg2.extras
from app.config.settings import settings
from app.utils.logger import log_info, log_error

def get_db_connection():
    """Obtiene conexión a la base de datos PostgreSQL"""
    try:
        connection = psycopg2.connect(
            settings.database_url,
            cursor_factory=psycopg2.extras.RealDictCursor
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
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    telefono VARCHAR(20) UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    user_type_id INTEGER NOT NULL DEFAULT 1,
                    municipality_id BIGINT,
                    avatar VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT chk_contact CHECK (email IS NOT NULL OR telefono IS NOT NULL)
                )
            """)
            
            # Tabla otp_codes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS otp_codes (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(100) NOT NULL,
                    otp_code VARCHAR(6) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Crear índices para otp_codes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_email_otp ON otp_codes(email, otp_code)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_expires ON otp_codes(expires_at)")
            
            # Tabla user_types
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_types (
                    id SERIAL PRIMARY KEY,
                    type_name VARCHAR(50) NOT NULL UNIQUE,
                    type_hash VARCHAR(64) NOT NULL UNIQUE,
                    description VARCHAR(200),
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insertar tipos de usuario por defecto solo si no existen
            cursor.execute("SELECT COUNT(*) FROM user_types")
            result = cursor.fetchone()
            user_types_count = result['count'] if result else 0
            
            if user_types_count == 0:
                cursor.execute("""
                    INSERT INTO user_types (type_name, type_hash, description) VALUES 
                    ('cliente', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', 'Usuario cliente final'),
                    ('negocio', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1', 'Usuario propietario de negocio'),
                    ('admin', 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1b2', 'Administrador del sistema')
                """)
                log_info("Tipos de usuario insertados")
            
            # Tabla municipalities
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS municipalities (
                    id BIGSERIAL PRIMARY KEY,
                    municipio VARCHAR(100) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla businesses
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS businesses (
                    id BIGSERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL UNIQUE,
                    category VARCHAR(100) NOT NULL,
                    address TEXT,
                    municipality_id BIGINT REFERENCES municipalities(id),
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    logo VARCHAR(500),
                    description TEXT,
                    rating DECIMAL(2,1) DEFAULT 0.0,
                    visits_for_prize INTEGER DEFAULT 6,
                    facebook VARCHAR(500),
                    instagram VARCHAR(500),
                    tiktok VARCHAR(500),
                    whatsapp VARCHAR(500),
                    owner_user_id INTEGER REFERENCES users(id),
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Agregar columna owner_user_id si no existe
            try:
                cursor.execute("ALTER TABLE businesses ADD COLUMN owner_user_id INTEGER REFERENCES users(id)")
            except:
                pass  # Ya existe
            
            # Tabla business_menu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS business_menu (
                    id BIGSERIAL PRIMARY KEY,
                    business_id BIGINT NOT NULL REFERENCES businesses(id),
                    producto VARCHAR(200) NOT NULL,
                    descripcion TEXT,
                    precio DECIMAL(10,2) NOT NULL,
                    categoria VARCHAR(100),
                    disponible BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla user_visits
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_visits (
                    id BIGSERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    business_id BIGINT NOT NULL REFERENCES businesses(id),
                    visit_date TIMESTAMP NOT NULL,
                    visit_month VARCHAR(7) NOT NULL,
                    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'cancelled')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Crear índice para user_visits
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_business_month ON user_visits(user_id, business_id, visit_month)")
            
            # Tabla user_rounds (Sistema de rondas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_rounds (
                    id BIGSERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    business_id BIGINT NOT NULL REFERENCES businesses(id),
                    round_number INTEGER NOT NULL DEFAULT 1,
                    progress_in_round INTEGER NOT NULL DEFAULT 0,
                    round_start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP NULL,
                    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
                    is_reward_claimed BOOLEAN NOT NULL DEFAULT FALSE,
                    last_visit_id BIGINT NULL
                )
            """)
            
            # Crear índices para user_rounds
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_rounds_user_business ON user_rounds(user_id, business_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_rounds_completed ON user_rounds(is_completed)")
            # Agregar foreign keys a users
            try:
                cursor.execute("ALTER TABLE users ADD CONSTRAINT fk_user_type FOREIGN KEY (user_type_id) REFERENCES user_types(id)")
            except:
                pass  # Ya existe
            
            try:
                cursor.execute("ALTER TABLE users ADD CONSTRAINT fk_municipality FOREIGN KEY (municipality_id) REFERENCES municipalities(id)")
            except:
                pass  # Ya existe
            
            # Insertar datos de prueba solo si no existen
            cursor.execute("SELECT COUNT(*) FROM municipalities")
            result = cursor.fetchone()
            municipality_count = result['count'] if result else 0
            
            if municipality_count == 0:
                cursor.execute("""
                    INSERT INTO municipalities (municipio, state) VALUES
                    ('Papantla', 'Veracruz'),
                    ('Coatzintla', 'Veracruz'),
                    ('Poza Rica', 'Veracruz'),
                    ('Tuxpan', 'Veracruz')
                """)
                log_info("Municipios de ejemplo insertados")
            
            cursor.execute("SELECT COUNT(*) FROM businesses")
            result = cursor.fetchone()
            business_count = result['count'] if result else 0
            
            if business_count == 0:
                # Primero crear un usuario admin por defecto
                cursor.execute("""
                    INSERT INTO users (nombre, email, password, user_type_id) VALUES
                    ('Administrador', 'admin@flevoapp.com', '$2b$12$LQv3c1yqBWVHxkd0LQ4YCOdHrCkUAI6H0O/8VfzCr5FqSQqIBfxSm', 3)
                    ON CONFLICT (email) DO NOTHING
                """)
                
                cursor.execute("""
                    INSERT INTO businesses (name, category, address, municipality_id, phone, email, description, rating, facebook, instagram, tiktok, whatsapp, owner_user_id) VALUES
                    ('Restaurante El Totonaco', 'Restaurante', 'Calle Enríquez 123, Centro', 1, '7841234567', 'contacto@eltotonaco.com', 'Comida tradicional veracruzana', 4.5, 'https://facebook.com/eltotonaco', 'https://instagram.com/eltotonaco', 'https://tiktok.com/@eltotonaco', 'https://wa.me/527841234567', 1),
                    ('Café Vanilla', 'Cafetería', 'Av. 20 de Noviembre 45', 2, '7822345678', 'info@cafevanilla.com', 'Café de especialidad y vainilla', 4.2, 'https://facebook.com/cafevanilla', 'https://instagram.com/cafevanilla', 'https://tiktok.com/@cafevanilla', 'https://wa.me/527822345678', 1),
                    ('Boutique Jarocha', 'Ropa', 'Plaza Poza Rica 67', 3, '7823456789', 'ventas@boutiquejarocha.com', 'Ropa y accesorios regionales', 4.0, 'https://facebook.com/boutiquejarocha', 'https://instagram.com/boutiquejarocha', 'https://tiktok.com/@boutiquejarocha', 'https://wa.me/527823456789', 1),
                    ('Farmacia del Puerto', 'Farmacia', 'Malecón Tuxpan 89', 4, '7834567890', 'contacto@farmaciapuerto.com', 'Medicamentos y productos de salud', 4.3, 'https://facebook.com/farmaciapuerto', 'https://instagram.com/farmaciapuerto', 'https://tiktok.com/@farmaciapuerto', 'https://wa.me/527834567890', 1),
                    ('Gimnasio Coatza Fit', 'Deportes', 'Calle Hidalgo 12', 2, '7825678901', 'info@coatzafit.com', 'Gimnasio y entrenamiento personal', 4.4, 'https://facebook.com/coatzafit', 'https://instagram.com/coatzafit', 'https://tiktok.com/@coatzafit', 'https://wa.me/527825678901', 1)
                """)
                log_info("Businesses de ejemplo insertados")
            
            cursor.execute("SELECT COUNT(*) FROM business_menu")
            result = cursor.fetchone()
            menu_count = result['count'] if result else 0
            
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
            
            connection.commit()
            log_info("Base de datos PostgreSQL inicializada correctamente")
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        log_error(f"Error inicializando base de datos: {str(e)}")
        raise
    finally:
        connection.close()