#!/usr/bin/env python3
"""
Script para crear la tabla de suscripciones push
"""
from app.models.push_subscription import PushSubscription

def main():
    print("Creando tabla push_subscriptions...")
    PushSubscription.create_table()
    print("Tabla creada exitosamente")

if __name__ == "__main__":
    main()