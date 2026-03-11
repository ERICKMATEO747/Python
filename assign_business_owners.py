#!/usr/bin/env python3
import sqlite3

def assign_owners_to_businesses():
    conn = sqlite3.connect('auth_api.db')
    cursor = conn.cursor()
    
    # Agregar columna owner_id si no existe
    try:
        cursor.execute('ALTER TABLE businesses ADD COLUMN owner_id INTEGER')
        print("Columna owner_id agregada a la tabla businesses")
    except sqlite3.OperationalError:
        print("Columna owner_id ya existe")
    
    # Asignar propietarios a los negocios
    # Carlos Hernández (ID: 3) será propietario de 3 negocios
    # Ana López (ID: 4) será propietaria de 3 negocios
    
    assignments = [
        (3, 1),  # Carlos -> Restaurante El Totonaco
        (3, 2),  # Carlos -> Café Vanilla  
        (3, 3),  # Carlos -> Pizzería Don Juan
        (4, 4),  # Ana -> Tacos El Buen Sabor
        (4, 5),  # Ana -> Heladería Tropical
        (4, 6),  # Ana -> Panadería La Espiga
    ]
    
    for owner_id, business_id in assignments:
        cursor.execute(
            'UPDATE businesses SET owner_id = ? WHERE id = ?',
            (owner_id, business_id)
        )
    
    conn.commit()
    
    # Mostrar resultado
    print("\n=== ASIGNACIONES REALIZADAS ===")
    cursor.execute('''
        SELECT 
            b.id,
            b.name,
            b.category,
            u.nombre as owner_name,
            u.email as owner_email
        FROM businesses b
        LEFT JOIN users u ON b.owner_id = u.id
        ORDER BY b.id
    ''')
    
    results = cursor.fetchall()
    
    for row in results:
        owner_info = f"{row[3]} ({row[4]})" if row[3] else "Sin propietario"
        print(f"{row[0]}: {row[1]} ({row[2]}) - Propietario: {owner_info}")
    
    conn.close()
    print("\n[OK] Propietarios asignados exitosamente")

if __name__ == "__main__":
    assign_owners_to_businesses()