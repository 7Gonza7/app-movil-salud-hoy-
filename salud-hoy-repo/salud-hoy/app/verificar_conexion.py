# -*- coding: utf-8 -*-
"""
Script para verificar que la conexión a la base de datos funciona correctamente
"""

from database import Database
import os

print("=" * 70)
print("  VERIFICACION DE CONEXION A BASE DE DATOS")
print("=" * 70)

# Conectar a la base de datos LOCAL del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(project_root, 'data', 'salud_hoy.db')

print(f"\n[1] Ruta de base de datos:")
print(f"    {db_path}")

try:
    db = Database(db_path)
    print("\n[2] Conexion: [OK]")
    
    # Verificar perfil
    perfil = db.get_profile()
    print(f"\n[3] Perfil actual:")
    print(f"    Nombre: {perfil['name']}")
    print(f"    Objetivo: {perfil['goal']}")
    
    # Verificar hábitos
    habitos = db.get_habits()
    print(f"\n[4] Habitos activos: {len(habitos)}")
    for h in habitos:
        print(f"    - {h['title']}")
    
    # Verificar días registrados
    dias = db.get_all_days_with_habits()
    print(f"\n[5] Dias con actividad: {len(dias)}")
    
    db.close()
    
    print("\n" + "=" * 70)
    print("  TODO FUNCIONA CORRECTAMENTE [OK]")
    print("=" * 70)
    
except Exception as e:
    print(f"\n[ERROR] Fallo la verificacion: {e}")
    print("\n" + "=" * 70)
    print("  HAY UN PROBLEMA CON LA CONEXION [ERROR]")
    print("=" * 70)

