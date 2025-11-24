# -*- coding: utf-8 -*-
"""
Pruebas de base de datos para Salud Hoy
Valida la conexión, creación de esquema y operaciones básicas
"""

import pytest
import os
import tempfile
import shutil
import sqlite3

# Importar las clases de base de datos
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'salud-hoy')))

from app.database import *
from app.auth_database import AuthDatabase


class TestDatabase:
    """Clase para probar funcionalidades de base de datos"""
    
    @pytest.fixture
    def temp_db(self):
        """Crea una base de datos temporal para las pruebas"""
        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_salud_hoy.db")
        
        # Crear instancia de Database
        db = Database(db_path)
        
        yield db, db_path
        
        # Limpiar después de las pruebas
        try:
            # Cerrar conexiones antes de limpiar
            if hasattr(db, 'close'):
                db.close()
            shutil.rmtree(temp_dir)
        except PermissionError:
            # En Windows, a veces los archivos están en uso
            # Los archivos temporales se limpiarán automáticamente
            pass
    
    def test_conexion_base_datos(self, temp_db):
        """
        Prueba que la conexión a la base de datos funcione correctamente
        Simula connect_db() creando el archivo salud_hoy.db
        """
        db, db_path = temp_db
        
        # Verificar que el archivo de base de datos se creó (simula connect_db())
        assert os.path.exists(db_path), "El archivo de base de datos debería existir"
        
        # Verificar que se puede obtener una conexión
        conn = db.get_connection()
        assert conn is not None, "Debería poder obtener una conexión a la base de datos"
        
        # Verificar que la conexión funciona ejecutando una consulta simple
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1, "La consulta debería devolver 1"
        
        conn.close()
    
    def test_esquema_tabla_users(self, temp_db):
        """
        Prueba que el esquema contenga la tabla users (de autenticación)
        Comprueba que la tabla users exista tras la conexión
        """
        # Crear base de datos de autenticación temporal
        temp_dir = tempfile.mkdtemp()
        auth_db_path = os.path.join(temp_dir, "test_users.db")
        
        try:
            auth_db = AuthDatabase(auth_db_path)
            
            # Verificar que la tabla users existe
            conn = auth_db.get_connection()
            cursor = conn.cursor()
            
            # Verificar que la tabla users existe
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='users'
            """)
            result = cursor.fetchone()
            assert result is not None, "La tabla 'users' debería existir"
            
            # Verificar la estructura de la tabla users
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            expected_columns = ['id', 'name', 'email', 'password', 'created_at']
            for col in expected_columns:
                assert col in column_names, f"La columna '{col}' debería existir en la tabla users"
            
            conn.close()
            
        finally:
            try:
                shutil.rmtree(temp_dir)
            except PermissionError:
                # En Windows, a veces los archivos están en uso
                pass
    
    def test_conexion_sin_errores(self, temp_db):
        """
        Prueba que la conexión no arroje errores
        Valida que la conexión no arroje errores
        """
        db, db_path = temp_db
        
        # Verificar que la conexión no arroja errores
        try:
            conn = db.get_connection()
            assert conn is not None, "La conexión debería establecerse sin errores"
            
            # Ejecutar una consulta simple para verificar que funciona
            cursor = conn.cursor()
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            assert result[0] == 1, "La consulta debería ejecutarse sin errores"
            
            conn.close()
            
        except Exception as e:
            pytest.fail(f"La conexión no debería arrojar errores: {e}")
    
    def test_esquema_tablas_principales(self, temp_db):
        """Prueba que el esquema contenga las tablas principales de la aplicación"""
        db, db_path = temp_db
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Verificar que las tablas principales existen
        expected_tables = [
            'usuario_perfil',
            'habito', 
            'dia',
            'habitos_dia'
        ]
        
        for table_name in expected_tables:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """, (table_name,))
            result = cursor.fetchone()
            assert result is not None, f"La tabla '{table_name}' debería existir"
        
        conn.close()
    
    def test_datos_iniciales_habitos(self, temp_db):
        """Prueba que se inserten los datos iniciales de hábitos"""
        db, db_path = temp_db
        
        # Obtener los hábitos activos
        habits = db.get_habits(active_only=True)
        
        # Verificar que existen hábitos
        assert len(habits) > 0, "Deberían existir hábitos iniciales"
        
        # Verificar que los hábitos tienen la estructura correcta
        for habit in habits:
            assert "key" in habit, "Cada hábito debería tener una clave"
            assert "title" in habit, "Cada hábito debería tener un título"
            assert habit["key"] is not None, "La clave del hábito no debería ser None"
            assert habit["title"] is not None, "El título del hábito no debería ser None"
        
        # Verificar que existen los hábitos esperados
        habit_keys = [habit["key"] for habit in habits]
        expected_habits = ["camina_10", "estirate_2", "respira_1", "postura_1"]
        
        for expected_habit in expected_habits:
            assert expected_habit in habit_keys, f"El hábito '{expected_habit}' debería existir"
    
    def test_perfil_usuario_inicial(self, temp_db):
        """Prueba que se cree el perfil de usuario inicial"""
        db, db_path = temp_db
        
        # Obtener el perfil
        profile = db.get_profile()
        
        # Verificar que el perfil existe y tiene la estructura correcta
        assert profile is not None, "Debería existir un perfil de usuario"
        assert "name" in profile, "El perfil debería tener un campo 'name'"
        assert "goal" in profile, "El perfil debería tener un campo 'goal'"
        
        # Verificar valores por defecto
        assert profile["name"] == "", "El nombre inicial debería estar vacío"
        assert profile["goal"] == "Moverme más", "El objetivo inicial debería ser 'Moverme más'"
    
    def test_operaciones_habitos_dia(self, temp_db):
        """Prueba las operaciones básicas con hábitos del día"""
        db, db_path = temp_db
        
        # Fecha de prueba
        test_date = "2025-01-15"
        
        # Asegurar que el día existe
        db.ensure_day_exists(test_date)
        
        # Obtener hábitos del día (inicialmente todos en False)
        day_habits = db.get_day_habits(test_date)
        assert isinstance(day_habits, dict), "Los hábitos del día deberían ser un diccionario"
        
        # Verificar que todos los hábitos están en False inicialmente
        for habit_key, done in day_habits.items():
            assert done == False, f"El hábito '{habit_key}' debería estar en False inicialmente"
        
        # Marcar un hábito como completado
        habit_key = "camina_10"
        db.set_habit_status(test_date, habit_key, True)
        
        # Verificar que el hábito se marcó como completado
        day_habits_after = db.get_day_habits(test_date)
        assert day_habits_after[habit_key] == True, "El hábito debería estar marcado como completado"
        
        # Verificar contador de completados
        completed_count = db.get_completed_count_for_day(test_date)
        assert completed_count == 1, "Debería haber 1 hábito completado"
    
    def test_actualizacion_perfil(self, temp_db):
        """Prueba la actualización del perfil de usuario"""
        db, db_path = temp_db
        
        # Datos del perfil a actualizar
        new_name = "Juan Pérez"
        new_goal = "Comer más saludable"
        
        # Actualizar perfil
        db.update_profile(new_name, new_goal)
        
        # Verificar que se actualizó correctamente
        updated_profile = db.get_profile()
        assert updated_profile["name"] == new_name, "El nombre debería haberse actualizado"
        assert updated_profile["goal"] == new_goal, "El objetivo debería haberse actualizado"
    
    def test_reset_datos(self, temp_db):
        """Prueba la función de reset de datos"""
        db, db_path = temp_db
        
        # Crear algunos datos de prueba
        test_date = "2025-01-15"
        db.ensure_day_exists(test_date)
        db.set_habit_status(test_date, "camina_10", True)
        db.update_profile("Usuario Test", "Objetivo Test")
        
        # Verificar que los datos existen
        day_habits = db.get_day_habits(test_date)
        assert day_habits["camina_10"] == True, "El hábito debería estar completado"
        
        profile = db.get_profile()
        assert profile["name"] == "Usuario Test", "El perfil debería tener los datos de prueba"
        
        # Resetear datos
        db.reset_all_data()
        
        # Verificar que los datos se resetearon
        day_habits_after = db.get_day_habits(test_date)
        assert day_habits_after["camina_10"] == False, "El hábito debería estar en False después del reset"
        
        profile_after = db.get_profile()
        assert profile_after["name"] == "", "El nombre debería estar vacío después del reset"
        assert profile_after["goal"] == "Moverme más", "El objetivo debería ser el por defecto después del reset"
