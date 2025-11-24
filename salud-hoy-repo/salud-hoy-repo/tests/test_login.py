# -*- coding: utf-8 -*-
"""
Pruebas de autenticación para Salud Hoy
Valida el login de usuarios existentes y manejo de credenciales incorrectas
"""

import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Importar las clases de autenticación
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'salud-hoy')))

from app.database import *
from app.auth_database import AuthDatabase


class TestLogin:
    """Clase para probar funcionalidades de login"""
    
    @pytest.fixture
    def temp_db(self):
        """Crea una base de datos temporal para las pruebas"""
        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_users.db")
        
        # Crear instancia de AuthDatabase
        auth_db = AuthDatabase(db_path)
        
        yield auth_db, db_path
        
        # Limpiar después de las pruebas
        try:
            # Cerrar conexiones antes de limpiar
            if hasattr(auth_db, 'close'):
                auth_db.close()
            shutil.rmtree(temp_dir)
        except PermissionError:
            # En Windows, a veces los archivos están en uso
            # Los archivos temporales se limpiarán automáticamente
            pass
    
    def test_login_credenciales_validas(self, temp_db):
        """
        Prueba que el login acepte credenciales válidas de usuario existente
        Verifica que al ingresar credenciales válidas retorne un usuario
        """
        auth_db, db_path = temp_db
        
        # Crear un usuario de prueba
        name = "Usuario Prueba"
        email = "test@example.com"
        password = "password123"
        
        # Registrar usuario usando add_user()
        success = auth_db.add_user(name, email, password)
        assert success == True, "El usuario debería registrarse correctamente"
        
        # Verificar que el usuario existe usando user_exists()
        user_exists = auth_db.user_exists(email)
        assert user_exists == True, "El usuario debería existir en la base de datos"
        
        # Intentar login con credenciales correctas usando check_user()
        user_data = auth_db.check_user(email, password)
        assert user_data is not None, "El login debería ser exitoso con credenciales válidas"
        assert user_data["name"] == name, "El nombre debería coincidir"
        assert user_data["email"] == email.lower(), "El email debería coincidir (en minúsculas)"
        assert "id" in user_data, "Debería incluir el ID del usuario"
    
    def test_login_credenciales_incorrectas(self, temp_db):
        """
        Prueba que el login rechace credenciales incorrectas
        Verifica que una contraseña incorrecta devuelva None
        """
        auth_db, db_path = temp_db
        
        # Crear un usuario de prueba
        auth_db.add_user("Usuario Prueba", "test@example.com", "password123")
        
        # Intentar login con contraseña incorrecta usando check_user()
        user_data = auth_db.check_user("test@example.com", "password_incorrecta")
        assert user_data is None, "El login debería fallar con contraseña incorrecta"
        
        # Intentar login con email incorrecto
        user_data = auth_db.check_user("otro@example.com", "password123")
        assert user_data is None, "El login debería fallar con email incorrecto"
        
        # Intentar login con ambos incorrectos
        user_data = auth_db.check_user("otro@example.com", "password_incorrecta")
        assert user_data is None, "El login debería fallar con credenciales completamente incorrectas"
    
    def test_login_usuario_inexistente(self, temp_db):
        """Prueba que el sistema maneje correctamente usuarios inexistentes"""
        auth_db, db_path = temp_db
        
        # Verificar que un usuario no existe
        user_exists = auth_db.user_exists("noexiste@example.com")
        assert user_exists == False, "El usuario no debería existir"
        
        # Intentar login con usuario inexistente
        user_data = auth_db.check_user("noexiste@example.com", "cualquier_password")
        assert user_data is None, "El login debería fallar para usuario inexistente"
    
    def test_login_campos_vacios(self, temp_db):
        """Prueba que el sistema maneje correctamente campos vacíos"""
        auth_db, db_path = temp_db
        
        # Intentar login con email vacío
        user_data = auth_db.check_user("", "password123")
        assert user_data is None, "El login debería fallar con email vacío"
        
        # Intentar login con contraseña vacía
        user_data = auth_db.check_user("test@example.com", "")
        assert user_data is None, "El login debería fallar con contraseña vacía"
        
        # Intentar login con ambos vacíos
        user_data = auth_db.check_user("", "")
        assert user_data is None, "El login debería fallar con ambos campos vacíos"
    
    def test_login_case_insensitive_email(self, temp_db):
        """Prueba que el login sea insensible a mayúsculas/minúsculas en el email"""
        auth_db, db_path = temp_db
        
        # Crear usuario con email en minúsculas
        auth_db.add_user("Usuario Prueba", "test@example.com", "password123")
        
        # Intentar login con email en mayúsculas
        user_data = auth_db.check_user("TEST@EXAMPLE.COM", "password123")
        assert user_data is not None, "El login debería funcionar con email en mayúsculas"
        assert user_data["email"] == "test@example.com", "El email debería normalizarse a minúsculas"
        
        # Intentar login con email mixto
        user_data = auth_db.check_user("Test@Example.Com", "password123")
        assert user_data is not None, "El login debería funcionar con email mixto"
    
    def test_login_espacios_en_email(self, temp_db):
        """Prueba que el sistema maneje correctamente espacios en el email"""
        auth_db, db_path = temp_db
        
        # Crear usuario
        auth_db.add_user("Usuario Prueba", "test@example.com", "password123")
        
        # Intentar login con espacios al inicio y final
        user_data = auth_db.check_user("  test@example.com  ", "password123")
        assert user_data is not None, "El login debería funcionar con espacios en el email"
        assert user_data["email"] == "test@example.com", "El email debería limpiarse de espacios"
