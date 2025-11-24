# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la conexión y funcionalidad de la base de datos
"""

import os
import tempfile
from datetime import date, timedelta
from app.database import Database


def test_database():
    """Ejecuta pruebas básicas de la base de datos"""
    
    print("=" * 60)
    print("  Pruebas de Base de Datos SQLite")
    print("  Salud Hoy")
    print("=" * 60)
    print()
    
    # Crear una base de datos temporal para pruebas
    temp_dir = tempfile.gettempdir()
    test_db_path = os.path.join(temp_dir, "test_salud_hoy.db")
    
    print(f"[*] Creando base de datos de prueba en: {test_db_path}")
    
    # Inicializar base de datos
    db = Database(test_db_path)
    print("[OK] Base de datos inicializada")
    print()
    
    # Test 1: Perfil
    print("[TEST 1] Perfil de usuario")
    print("   - Obteniendo perfil inicial...")
    profile = db.get_profile()
    print(f"   - Perfil: {profile}")
    
    print("   - Actualizando perfil...")
    db.update_profile("Usuario Test", "Estar más saludable")
    profile = db.get_profile()
    print(f"   - Perfil actualizado: {profile}")
    assert profile["name"] == "Usuario Test"
    assert profile["goal"] == "Estar más saludable"
    print("   [PASS] Test de perfil pasado")
    print()
    
    # Test 2: Hábitos
    print("[TEST 2] Catálogo de hábitos")
    habits = db.get_habits()
    print(f"   - Hábitos encontrados: {len(habits)}")
    for habit in habits:
        print(f"     * {habit['title']} ({habit['key']})")
    assert len(habits) == 4
    print("   [PASS] Test de hábitos pasado")
    print()
    
    # Test 3: Registro diario
    print("[TEST 3] Registro de hábitos diarios")
    today_str = date.today().isoformat()
    print(f"   - Fecha: {today_str}")
    
    print("   - Marcando hábitos como completados...")
    db.set_habit_status(today_str, "camina_10", True)
    db.set_habit_status(today_str, "estirate_2", True)
    
    habits_today = db.get_day_habits(today_str)
    print(f"   - Hábitos de hoy: {habits_today}")
    assert habits_today["camina_10"] == True
    assert habits_today["estirate_2"] == True
    assert habits_today["respira_1"] == False
    
    completed = db.get_completed_count_for_day(today_str)
    print(f"   - Completados hoy: {completed}/4")
    assert completed == 2
    print("   [PASS] Test de registro diario pasado")
    print()
    
    # Test 4: Racha
    print("[TEST 4] Cálculo de racha")
    
    # Simular 3 días de actividad
    for i in range(3):
        day = (date.today() - timedelta(days=i)).isoformat()
        db.set_habit_status(day, "camina_10", True)
    
    streak = db.get_streak(threshold=1)
    print(f"   - Racha actual: {streak} día(s)")
    assert streak >= 3
    print("   [PASS] Test de racha pasado")
    print()
    
    # Test 5: Estadísticas mensuales
    print("[TEST 5] Días activos del mes")
    today = date.today()
    active_days = db.get_monthly_active_days(today.year, today.month)
    print(f"   - Días activos este mes: {active_days}")
    assert active_days >= 1
    print("   [PASS] Test de estadísticas mensuales pasado")
    print()
    
    # Test 6: Reset de datos
    print("[TEST 6] Reseteo de datos")
    print("   - Reseteando todos los datos...")
    db.reset_all_data()
    
    habits_after_reset = db.get_day_habits(today_str)
    all_false = all(not v for v in habits_after_reset.values())
    print(f"   - Todos los hábitos en False: {all_false}")
    assert all_false
    print("   [PASS] Test de reseteo pasado")
    print()
    
    # Cerrar conexión
    db.close()
    print("[*] Conexión cerrada")
    print()
    
    # Limpiar archivo de prueba
    try:
        os.remove(test_db_path)
        print(f"[*] Archivo de prueba eliminado: {test_db_path}")
    except:
        pass
    
    print()
    print("=" * 60)
    print("  *** Todas las pruebas pasaron exitosamente! ***")
    print("=" * 60)
    print()
    print("La base de datos SQLite está funcionando correctamente.")
    print("Puedes ejecutar la aplicación con confianza.")


def main():
    try:
        test_database()
    except AssertionError as e:
        print()
        print("[ERROR] Una o más pruebas fallaron")
        print(f"   Detalle: {e}")
    except Exception as e:
        print()
        print("[ERROR] ERROR INESPERADO:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

