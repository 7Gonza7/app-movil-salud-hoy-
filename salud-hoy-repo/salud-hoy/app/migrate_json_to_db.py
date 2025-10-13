# -*- coding: utf-8 -*-
"""
Script de migración: JSON a SQLite
Convierte datos antiguos de salud_hoy_data.json a la nueva base de datos SQLite
"""

import os
import json
from database import Database


def migrate_json_to_sqlite(json_path, db_path):
    """
    Migra datos desde JSON a SQLite
    
    :param json_path: Ruta al archivo JSON antiguo
    :param db_path: Ruta al archivo de base de datos SQLite
    """
    
    # Verificar que existe el archivo JSON
    if not os.path.exists(json_path):
        print(f"❌ No se encontró el archivo JSON: {json_path}")
        return False
    
    print(f"📖 Leyendo datos de: {json_path}")
    
    # Cargar datos JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error al leer JSON: {e}")
        return False
    
    print(f"✅ Datos JSON cargados correctamente")
    
    # Inicializar base de datos
    print(f"🗄️  Inicializando base de datos: {db_path}")
    db = Database(db_path)
    
    # Migrar perfil
    profile = data.get("profile", {})
    if profile:
        name = profile.get("name", "")
        goal = profile.get("goal", "Moverme más")
        db.update_profile(name, goal)
        print(f"✅ Perfil migrado: {name if name else '(sin nombre)'}, Objetivo: {goal}")
    
    # Migrar días y hábitos
    days = data.get("days", {})
    total_days = len(days)
    total_habits_migrated = 0
    
    if days:
        print(f"📅 Migrando {total_days} día(s)...")
        
        for day_date, day_data in days.items():
            # Asegurar que existe el día
            db.ensure_day_exists(day_date)
            
            # Migrar hábitos del día
            habits = day_data.get("habits", {})
            for habit_key, done in habits.items():
                if done:  # Solo migrar los hábitos completados
                    db.set_habit_status(day_date, habit_key, done)
                    total_habits_migrated += 1
        
        print(f"✅ {total_habits_migrated} hábito(s) completado(s) migrado(s)")
    
    # Cerrar conexión
    db.close()
    
    print("\n✨ ¡Migración completada exitosamente!")
    print(f"   - Perfil: ✅")
    print(f"   - Días: {total_days}")
    print(f"   - Hábitos completados: {total_habits_migrated}")
    
    return True


def main():
    """Función principal del script de migración"""
    print("=" * 60)
    print("  Script de Migración: JSON → SQLite")
    print("  Salud Hoy")
    print("=" * 60)
    print()
    
    # Detectar rutas automáticamente
    # Asumiendo que el script se ejecuta desde la carpeta app/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Pedir al usuario la ubicación del archivo JSON
    print("📍 Ubicaciones comunes de datos:")
    print("   1. Windows: C:\\Users\\<usuario>\\AppData\\Local\\SaludHoyApp")
    print("   2. Linux: ~/.local/share/SaludHoyApp")
    print("   3. Mac: ~/Library/Application Support/SaludHoyApp")
    print()
    
    json_path = input("Ingresa la ruta completa al archivo salud_hoy_data.json: ").strip()
    
    if not json_path:
        print("❌ No se ingresó ninguna ruta. Abortando.")
        return
    
    # Ruta de la base de datos (en la misma ubicación que el JSON)
    json_dir = os.path.dirname(json_path)
    db_path = os.path.join(json_dir, "salud_hoy.db")
    
    print()
    print(f"🔄 Migrando de:")
    print(f"   JSON: {json_path}")
    print(f"   a DB: {db_path}")
    print()
    
    # Confirmar
    confirm = input("¿Continuar con la migración? (s/n): ").strip().lower()
    if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Migración cancelada.")
        return
    
    print()
    
    # Ejecutar migración
    success = migrate_json_to_sqlite(json_path, db_path)
    
    if success:
        print()
        print("💾 La base de datos SQLite está lista para usar.")
        print("   Puedes ejecutar la aplicación normalmente ahora.")
        print()
        backup_option = input("¿Deseas crear una copia de respaldo del JSON? (s/n): ").strip().lower()
        if backup_option in ['s', 'si', 'sí', 'y', 'yes']:
            backup_path = json_path + ".backup"
            try:
                import shutil
                shutil.copy2(json_path, backup_path)
                print(f"✅ Copia de respaldo creada: {backup_path}")
            except Exception as e:
                print(f"❌ Error al crear respaldo: {e}")


if __name__ == "__main__":
    main()




