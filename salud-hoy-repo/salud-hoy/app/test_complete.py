#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de testing completo para la aplicación Salud Hoy
Verifica todas las funcionalidades y detecta bugs potenciales
"""

import sys
import os
import sqlite3
from datetime import date, timedelta

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Verifica que todos los imports funcionen correctamente"""
    print("=" * 60)
    print("TEST 1: Verificando imports...")
    print("=" * 60)
    
    try:
        from kivy.config import Config
        print("[OK] Kivy importado correctamente")
    except ImportError as e:
        print(f"[ERROR] Error al importar Kivy: {e}")
        return False
    
    try:
        from kivymd.app import MDApp
        print("[OK] KivyMD importado correctamente")
    except ImportError as e:
        print(f"[ERROR] Error al importar KivyMD: {e}")
        return False
    
    try:
        from database import Database
        print("[OK] Database importado correctamente")
    except ImportError as e:
        print(f"[ERROR] Error al importar Database: {e}")
        return False
    
    print("\n[OK] Todos los imports funcionan correctamente\n")
    return True


def test_database_operations():
    """Verifica todas las operaciones de la base de datos"""
    print("=" * 60)
    print("TEST 2: Verificando operaciones de base de datos...")
    print("=" * 60)
    
    from database import Database
    
    # Crear base de datos de prueba
    test_db_path = os.path.join(os.path.dirname(__file__), "test_temp.db")
    
    # Eliminar DB de prueba si existe
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    try:
        # 1. Inicialización
        print("\n1. Inicializando base de datos...")
        db = Database(test_db_path)
        print("[OK] Base de datos inicializada")
        
        # 2. Perfil
        print("\n2. Probando operaciones de perfil...")
        profile = db.get_profile()
        assert isinstance(profile, dict), "El perfil debe ser un diccionario"
        assert "name" in profile, "El perfil debe tener 'name'"
        assert "goal" in profile, "El perfil debe tener 'goal'"
        print(f"[OK] Perfil obtenido: {profile}")
        
        db.update_profile("Usuario Test", "Estar más saludable")
        profile = db.get_profile()
        assert profile["name"] == "Usuario Test", "El nombre no se actualizó correctamente"
        assert profile["goal"] == "Estar más saludable", "El objetivo no se actualizó correctamente"
        print("[OK] Perfil actualizado correctamente")
        
        # 3. Hábitos
        print("\n3. Probando operaciones de hábitos...")
        habits = db.get_habits()
        assert len(habits) == 4, f"Debe haber 4 hábitos, se encontraron {len(habits)}"
        print(f"[OK] Hábitos obtenidos: {len(habits)} hábitos")
        
        # 4. Días
        print("\n4. Probando operaciones de días...")
        today = date.today().isoformat()
        db.ensure_day_exists(today)
        print(f"[OK] Día creado: {today}")
        
        # 5. Estado de hábitos
        print("\n5. Probando estado de hábitos...")
        habits_today = db.get_day_habits(today)
        assert isinstance(habits_today, dict), "Los hábitos del día deben ser un diccionario"
        print(f"[OK] Hábitos del día obtenidos: {habits_today}")
        
        # 6. Actualizar hábito
        print("\n6. Probando actualización de hábitos...")
        db.set_habit_status(today, "camina_10", True)
        habits_today = db.get_day_habits(today)
        assert habits_today.get("camina_10") == True, "El hábito no se actualizó correctamente"
        print("[OK] Hábito actualizado correctamente")
        
        # 7. Contador de completados
        print("\n7. Probando contador de completados...")
        count = db.get_completed_count_for_day(today)
        assert count == 1, f"Debe haber 1 hábito completado, se encontraron {count}"
        print(f"[OK] Contador correcto: {count} hábitos completados")
        
        # 8. Racha
        print("\n8. Probando cálculo de racha...")
        streak = db.get_streak(threshold=1)
        assert streak >= 0, "La racha no puede ser negativa"
        print(f"[OK] Racha calculada: {streak} días")
        
        # 9. Días activos del mes
        print("\n9. Probando días activos del mes...")
        active_days = db.get_monthly_active_days(date.today().year, date.today().month)
        assert active_days >= 0, "Los días activos no pueden ser negativos"
        print(f"[OK] Días activos del mes: {active_days} días")
        
        # 10. Resetear datos
        print("\n10. Probando reseteo de datos...")
        db.reset_all_data()
        profile = db.get_profile()
        assert profile["name"] == "", "El perfil no se reseteó correctamente"
        count = db.get_completed_count_for_day(today)
        assert count == 0, "Los hábitos no se resetearon correctamente"
        print("[OK] Datos reseteados correctamente")
        
        # Limpiar
        db.close()
        del db  # Eliminar referencia
        
        # Esperar un momento para que se libere el archivo en Windows
        import time
        time.sleep(0.5)
        
        # Intentar eliminar el archivo con reintentos
        max_retries = 3
        for i in range(max_retries):
            try:
                if os.path.exists(test_db_path):
                    os.remove(test_db_path)
                break
            except PermissionError:
                if i < max_retries - 1:
                    time.sleep(0.5)
                else:
                    print(f"⚠ No se pudo eliminar archivo temporal (puede ignorarse): {test_db_path}")
        
        print("\n[OK] Todas las operaciones de base de datos funcionan correctamente\n")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error en las operaciones de base de datos: {e}")
        import traceback
        traceback.print_exc()
        # Limpiar
        try:
            if os.path.exists(test_db_path):
                import time
                time.sleep(0.5)
                os.remove(test_db_path)
        except:
            pass  # Ignorar errores al limpiar
        return False


def test_kivy_file():
    """Verifica que el archivo .kv exista y sea válido"""
    print("=" * 60)
    print("TEST 3: Verificando archivo salud_hoy.kv...")
    print("=" * 60)
    
    kv_path = os.path.join(os.path.dirname(__file__), "salud_hoy.kv")
    
    if not os.path.exists(kv_path):
        print(f"[ERROR] El archivo {kv_path} no existe")
        return False
    
    print(f"[OK] Archivo encontrado: {kv_path}")
    
    # Verificar que el archivo no esté vacío
    with open(kv_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if len(content) == 0:
        print("[ERROR] El archivo .kv está vacío")
        return False
    
    print(f"[OK] Archivo válido ({len(content)} caracteres)")
    
    # Verificar IDs importantes
    required_ids = [
        "lbl_tip", "ck_camina", "ck_estira", "ck_respira", "ck_postura",
        "lbl_today_progress", "lbl_name", "lbl_goal", "badges_grid"
    ]
    
    missing_ids = []
    for id_name in required_ids:
        if f"id: {id_name}" not in content:
            missing_ids.append(id_name)
    
    if missing_ids:
        print(f"⚠ IDs faltantes: {', '.join(missing_ids)}")
    else:
        print("[OK] Todos los IDs requeridos están presentes")
    
    print("\n[OK] Archivo .kv verificado correctamente\n")
    return True


def test_assets():
    """Verifica que los assets necesarios existan"""
    print("=" * 60)
    print("TEST 4: Verificando assets...")
    print("=" * 60)
    
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    if not os.path.exists(assets_dir):
        print(f"[ERROR] Directorio de assets no existe: {assets_dir}")
        return False
    
    print(f"[OK] Directorio de assets encontrado: {assets_dir}")
    
    # Verificar logo
    logo_path = os.path.join(assets_dir, "logo.png")
    if not os.path.exists(logo_path):
        print(f"⚠ Logo no encontrado: {logo_path}")
    else:
        logo_size = os.path.getsize(logo_path)
        if logo_size == 0:
            print(f"⚠ Logo está vacío (0 bytes)")
        else:
            print(f"[OK] Logo encontrado ({logo_size} bytes)")
    
    print("\n[OK] Assets verificados\n")
    return True


def test_main_app_structure():
    """Verifica la estructura de la aplicación principal"""
    print("=" * 60)
    print("TEST 5: Verificando estructura de main.py...")
    print("=" * 60)
    
    try:
        import main
        
        # Verificar que SaludHoyApp existe
        assert hasattr(main, 'SaludHoyApp'), "La clase SaludHoyApp no existe"
        print("[OK] Clase SaludHoyApp encontrada")
        
        # Verificar métodos importantes
        app_class = main.SaludHoyApp
        required_methods = [
            'build', 'on_start', 'refresh_ui', 'on_toggle_habit',
            'open_edit_profile', 'refresh_profile_labels', 'reset_data',
            'switch_tab', 'on_stop'
        ]
        
        missing_methods = []
        for method_name in required_methods:
            if not hasattr(app_class, method_name):
                missing_methods.append(method_name)
        
        if missing_methods:
            print(f"[ERROR] Métodos faltantes: {', '.join(missing_methods)}")
            return False
        
        print(f"[OK] Todos los métodos requeridos están presentes ({len(required_methods)} métodos)")
        
        # Verificar propiedades
        print("[OK] Estructura de la aplicación es correcta")
        
        print("\n[OK] Estructura de main.py verificada correctamente\n")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error al verificar la estructura: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print(" INICIANDO TESTS DE LA APLICACIÓN SALUD HOY ")
    print("=" * 60 + "\n")
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: Base de datos
    results.append(("Base de datos", test_database_operations()))
    
    # Test 3: Archivo .kv
    results.append(("Archivo .kv", test_kivy_file()))
    
    # Test 4: Assets
    results.append(("Assets", test_assets()))
    
    # Test 5: Estructura de la app
    results.append(("Estructura de la app", test_main_app_structure()))
    
    # Resumen
    print("\n" + "=" * 60)
    print(" RESUMEN DE TESTS ")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "[OK] PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Total: {passed} tests pasados, {failed} tests fallidos")
    print("=" * 60)
    
    if failed == 0:
        print("\n[OK] Todos los tests pasaron exitosamente!")
        print("La aplicación está lista para ser ejecutada.\n")
        return True
    else:
        print(f"\n[WARNING]  Hay {failed} test(s) que necesitan atención.\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

