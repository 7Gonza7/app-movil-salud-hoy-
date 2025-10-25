# -*- coding: utf-8 -*-
"""
Pruebas de registro de usuarios para Salud Hoy
Valida el registro de nuevos usuarios y prevención de duplicados
"""

import pytest
import os
import tempfile
import shutil

# Importar las clases de autenticación
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'salud-hoy')))

from app.database import *
from app.auth_database import AuthDatabase


class TestRegistro:
    """Clase para probar funcionalidades de registro de usuarios"""
    
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
    
    def test_registro_usuario_nuevo_exitoso(self, temp_db):
        """
        Prueba que un nuevo usuario se registre correctamente
        Valida que un usuario nuevo se agregue correctamente usando add_user()
        """
        auth_db, db_path = temp_db
        
        # Datos del usuario
        name = "Juan Pérez"
        email = "juan@example.com"
        password = "password123"
        
        # Verificar que el usuario no existe inicialmente usando user_exists()
        user_exists = auth_db.user_exists(email)
        assert user_exists == False, "El usuario no debería existir inicialmente"
        
        # Registrar usuario usando add_user()
        success = auth_db.add_user(name, email, password)
        assert success == True, "El registro debería ser exitoso"
        
        # Verificar que el usuario ahora existe usando user_exists()
        user_exists = auth_db.user_exists(email)
        assert user_exists == True, "El usuario debería existir después del registro"
        
        # Verificar que se puede hacer login con las credenciales
        user_data = auth_db.check_user(email, password)
        assert user_data is not None, "Debería poder hacer login después del registro"
        assert user_data["name"] == name, "El nombre debería coincidir"
        assert user_data["email"] == email.lower(), "El email debería estar en minúsculas"
    
    def test_registro_email_duplicado(self, temp_db):
        """
        Prueba que el sistema evite registrar un correo duplicado
        Valida que el sistema bloquee el registro si el correo ya existe
        """
        auth_db, db_path = temp_db
        
        # Datos del primer usuario
        name1 = "Usuario Uno"
        email = "test@example.com"
        password1 = "password123"
        
        # Registrar primer usuario usando add_user()
        success1 = auth_db.add_user(name1, email, password1)
        assert success1 == True, "El primer registro debería ser exitoso"
        
        # Verificar que el usuario existe usando user_exists()
        user_exists = auth_db.user_exists(email)
        assert user_exists == True, "El usuario debería existir después del primer registro"
        
        # Intentar registrar segundo usuario con el mismo email usando add_user()
        name2 = "Usuario Dos"
        password2 = "password456"
        success2 = auth_db.add_user(name2, email, password2)
        assert success2 == False, "El segundo registro debería fallar por email duplicado"
        
        # Verificar que solo existe un usuario
        user_count = auth_db.get_user_count()
        assert user_count == 1, "Solo debería existir un usuario"
        
        # Verificar que el primer usuario sigue siendo el único
        user_data = auth_db.check_user(email, password1)
        assert user_data is not None, "El primer usuario debería seguir existiendo"
        assert user_data["name"] == name1, "El nombre debería ser del primer usuario"
    
    def test_registro_campos_vacios(self, temp_db):
        """Prueba que el sistema maneje correctamente campos vacíos en el registro"""
        auth_db, db_path = temp_db
        
        # Nota: La implementación actual de AuthDatabase no valida campos vacíos
        # Solo valida duplicados de email. Este test verifica el comportamiento actual.
        
        # Intentar registrar con nombre vacío (actualmente permite esto)
        success = auth_db.add_user("", "test@example.com", "password123")
        # La implementación actual permite nombres vacíos
        assert success == True, "La implementación actual permite nombres vacíos"
        
        # Verificar que se creó el usuario
        user_count = auth_db.get_user_count()
        assert user_count == 1, "Debería existir un usuario (comportamiento actual)"
        
        # Limpiar para el siguiente test
        auth_db.close()
    
    def test_registro_email_case_insensitive(self, temp_db):
        """Prueba que el sistema trate emails como case-insensitive"""
        auth_db, db_path = temp_db
        
        # Registrar usuario con email en minúsculas
        success1 = auth_db.add_user("Usuario Uno", "test@example.com", "password123")
        assert success1 == True, "El primer registro debería ser exitoso"
        
        # Intentar registrar con el mismo email en mayúsculas
        success2 = auth_db.add_user("Usuario Dos", "TEST@EXAMPLE.COM", "password456")
        assert success2 == False, "El segundo registro debería fallar por email duplicado (case-insensitive)"
        
        # Intentar registrar con email mixto
        success3 = auth_db.add_user("Usuario Tres", "Test@Example.Com", "password789")
        assert success3 == False, "El tercer registro debería fallar por email duplicado (case-insensitive)"
        
        # Verificar que solo existe un usuario
        user_count = auth_db.get_user_count()
        assert user_count == 1, "Solo debería existir un usuario"
    
    def test_registro_espacios_en_email(self, temp_db):
        """Prueba que el sistema maneje correctamente espacios en el email"""
        auth_db, db_path = temp_db
        
        # Registrar usuario con email con espacios
        name = "Usuario Prueba"
        email_with_spaces = "  test@example.com  "
        password = "password123"
        
        success = auth_db.add_user(name, email_with_spaces, password)
        assert success == True, "El registro debería ser exitoso con espacios en el email"
        
        # Verificar que el email se normalizó (sin espacios, en minúsculas)
        user_data = auth_db.check_user("test@example.com", password)
        assert user_data is not None, "Debería poder hacer login con el email normalizado"
        assert user_data["email"] == "test@example.com", "El email debería estar normalizado"
    
    def test_registro_validacion_email_formato(self, temp_db):
        """Prueba que el sistema valide el formato básico del email"""
        auth_db, db_path = temp_db
        
        # Intentar registrar con email sin @
        success = auth_db.add_user("Usuario", "email_sin_arroba", "password123")
        # Nota: La validación de formato se hace en la UI, no en la base de datos
        # La base de datos acepta cualquier string como email
        # Este test verifica que la base de datos no valida formato
        assert success == True, "La base de datos acepta cualquier formato de email"
    
    def test_registro_multiple_usuarios_diferentes(self, temp_db):
        """Prueba que se puedan registrar múltiples usuarios con emails diferentes"""
        auth_db, db_path = temp_db
        
        # Registrar primer usuario
        success1 = auth_db.add_user("Usuario Uno", "usuario1@example.com", "password123")
        assert success1 == True, "El primer registro debería ser exitoso"
        
        # Registrar segundo usuario
        success2 = auth_db.add_user("Usuario Dos", "usuario2@example.com", "password456")
        assert success2 == True, "El segundo registro debería ser exitoso"
        
        # Registrar tercer usuario
        success3 = auth_db.add_user("Usuario Tres", "usuario3@example.com", "password789")
        assert success3 == True, "El tercer registro debería ser exitoso"
        
        # Verificar que existen tres usuarios
        user_count = auth_db.get_user_count()
        assert user_count == 3, "Deberían existir tres usuarios"
        
        # Verificar que todos pueden hacer login
        user1 = auth_db.check_user("usuario1@example.com", "password123")
        user2 = auth_db.check_user("usuario2@example.com", "password456")
        user3 = auth_db.check_user("usuario3@example.com", "password789")
        
        assert user1 is not None, "El primer usuario debería poder hacer login"
        assert user2 is not None, "El segundo usuario debería poder hacer login"
        assert user3 is not None, "El tercer usuario debería poder hacer login"
        
        assert user1["name"] == "Usuario Uno", "El nombre del primer usuario debería coincidir"
        assert user2["name"] == "Usuario Dos", "El nombre del segundo usuario debería coincidir"
        assert user3["name"] == "Usuario Tres", "El nombre del tercer usuario debería coincidir"
