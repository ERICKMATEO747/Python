#!/usr/bin/env python3
"""
Script para generar claves VAPID para notificaciones push
"""
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import base64

def generate_vapid_keys():
    """Genera claves VAPID públicas y privadas"""
    
    # Generar clave privada
    private_key = ec.generate_private_key(ec.SECP256R1())
    
    # Obtener clave pública
    public_key = private_key.public_key()
    
    # Serializar clave privada
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serializar clave pública en formato raw
    public_raw = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    
    # Convertir a base64 URL-safe
    private_key_b64 = base64.urlsafe_b64encode(private_pem).decode('utf-8').rstrip('=')
    public_key_b64 = base64.urlsafe_b64encode(public_raw).decode('utf-8').rstrip('=')
    
    print("=== CLAVES VAPID GENERADAS ===")
    print(f"VAPID_PUBLIC_KEY={public_key_b64}")
    print(f"VAPID_PRIVATE_KEY={private_key_b64}")
    print(f"VAPID_SUBJECT=mailto:flevoapp@gmail.com")
    print("\nAgrega estas variables a tu archivo .env")

if __name__ == "__main__":
    generate_vapid_keys()