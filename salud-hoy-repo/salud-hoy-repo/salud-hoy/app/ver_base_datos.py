# -*- coding: utf-8 -*-
"""
Script para ver el contenido de la base de datos
"""

import sqlite3
import os

# Ubicación de la base de datos LOCAL del proyecto
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
db_path = os.path.join(project_dir, 'data', 'salud_hoy.db')

print("=" * 70)
print("  VISUALIZADOR DE BASE DE DATOS - SALUD HOY")
print("=" * 70)
print(f"\nUbicacion: {db_path}")

# Verificar si existe
if not os.path.exists(db_path):
    print("\n[!] La base de datos NO existe todavia.")
    print("    Ejecuta la aplicacion primero: python main.py")
    print("    Esto creara el archivo salud_hoy.db automaticamente.")
    exit()

print("[OK] Base de datos encontrada!")
print(f"Tamano: {os.path.getsize(db_path)} bytes")

# Conectar a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n" + "=" * 70)
print("  TABLAS")
print("=" * 70)

# Obtener lista de tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

print(f"\nTablas encontradas: {len(tablas)}")
for tabla in tablas:
    print(f"  - {tabla[0]}")

# Ver contenido de cada tabla
for tabla in tablas:
    nombre_tabla = tabla[0]
    print("\n" + "=" * 70)
    print(f"  TABLA: {nombre_tabla}")
    print("=" * 70)
    
    # Obtener estructura
    cursor.execute(f"PRAGMA table_info({nombre_tabla});")
    columnas = cursor.fetchall()
    
    print("\nColumnas:")
    for col in columnas:
        print(f"  - {col[1]} ({col[2]})")
    
    # Contar registros
    cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla};")
    count = cursor.fetchone()[0]
    print(f"\nRegistros: {count}")
    
    # Mostrar datos
    if count > 0:
        cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT 10;")
        registros = cursor.fetchall()
        
        print("\nDatos:")
        for i, registro in enumerate(registros, 1):
            print(f"  {i}. {registro}")

conn.close()

print("\n" + "=" * 70)
print("  FIN DEL REPORTE")
print("=" * 70)




