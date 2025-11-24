# -*- coding: utf-8 -*-
"""
Script para crear la base de datos manualmente
"""

from app.database import Database
import os

# Crear la ruta donde va la base de datos
db_path = os.path.join(
    os.path.expanduser('~'),
    'AppData', 'Local', 'SaludHoyApp', 'salud_hoy.db'
)

print("=" * 60)
print("  CREANDO BASE DE DATOS")
print("=" * 60)
print(f"\nUbicacion: {db_path}")

# Crear la base de datos
db = Database(db_path)

print("[OK] Base de datos creada!")
print("[OK] Tablas inicializadas!")
print("[OK] Datos por defecto insertados!")

# Verificar
profile = db.get_profile()
print(f"\n[INFO] Perfil inicial: {profile}")

habits = db.get_habits()
print(f"[INFO] Habitos cargados: {len(habits)}")

db.close()

print("\n" + "=" * 60)
print("  LISTO!")
print("=" * 60)
print("\nAhora puedes ejecutar: python ver_base_datos.py")




