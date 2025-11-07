#!/usr/bin/env python3
"""
Migration script to remove qr_code column from user_visits table
Since QR codes are no longer stored in database, only generated on demand
"""

import pymysql
from app.config.settings import settings

def remove_qr_code_column():
    """Remove qr_code column from user_visits table"""
    
    # Parse database URL
    db_url = settings.database_url
    # Extract connection details from mysql+pymysql://user:password@host:port/database
    db_url = db_url.replace('mysql+pymysql://', '')
    user_pass, host_db = db_url.split('@')
    user, password = user_pass.split(':')
    host_port, database = host_db.split('/')
    host, port = host_port.split(':')
    
    connection = pymysql.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database,
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            # Check if qr_code column exists
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'user_visits' 
                AND COLUMN_NAME = 'qr_code'
            """, (database,))
            
            if cursor.fetchone()[0] > 0:
                print("Removing qr_code column from user_visits table...")
                cursor.execute("ALTER TABLE user_visits DROP COLUMN qr_code")
                connection.commit()
                print("qr_code column removed successfully")
            else:
                print("qr_code column does not exist")
                
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    remove_qr_code_column()