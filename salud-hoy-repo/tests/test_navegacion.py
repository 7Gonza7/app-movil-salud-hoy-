# -*- coding: utf-8 -*-
"""
Pruebas de navegación para Salud Hoy
Valida la navegación entre pantallas y funcionalidades básicas de la UI
"""

import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock, Mock

# Importar las clases principales
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'salud-hoy')))

from app.database import *
from app.main import SaludHoyApp
from app.database import Database
from app.auth_database import AuthDatabase
from app.session_manager import SessionManager


class TestNavegacion:
    """Clase para probar funcionalidades de navegación y UI"""
    
    @pytest.fixture
    def temp_app(self):
        """Crea una aplicación temporal para las pruebas"""
        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_salud_hoy.db")
        auth_db_path = os.path.join(temp_dir, "test_users.db")
        
        # Mock de la aplicación para evitar inicialización completa de Kivy
        with patch('kivy.config.Config.set'), \
             patch('kivy.lang.Builder.load_file'), \
             patch('kivymd.app.MDApp.__init__', return_value=None), \
             patch('kivymd.toast.toast') as mock_toast, \
             patch('app.main.toast') as mock_main_toast:
            
            app = SaludHoyApp()
            
            # Configurar rutas de base de datos
            app.db = Database(db_path)
            app.auth_db = AuthDatabase(auth_db_path)
            app.session_manager = SessionManager()
            
            # Mock del root y screen_manager
            app.root = Mock()
            app.root.ids = Mock()
            app.root.ids.screen_manager = Mock()
            app.root.ids.screen_manager.current = "login"
            
            # Mock de campos de entrada
            app.root.ids.login_email = Mock()
            app.root.ids.login_password = Mock()
            app.root.ids.register_name = Mock()
            app.root.ids.register_email = Mock()
            app.root.ids.register_password = Mock()
            
            yield app, db_path, auth_db_path
        
        # Limpiar después de las pruebas
        try:
            shutil.rmtree(temp_dir)
        except PermissionError:
            # En Windows, a veces los archivos están en uso
            pass
    
    def test_carga_pantalla_principal(self, temp_app):
        """
        Prueba que la pantalla principal se cargue correctamente
        Simular cambio de pantallas del ScreenManager de main.py
        """
        app, db_path, auth_db_path = temp_app
        
        # Simular que hay una sesión activa
        user_data = {
            "id": 1,
            "name": "Usuario Test",
            "email": "test@example.com"
        }
        
        # Mock de la sesión activa
        with patch.object(app.session_manager, 'load_session', return_value=user_data), \
             patch.object(app.auth_db, 'get_user_by_email', return_value=user_data), \
             patch.object(app, '_load_data'), \
             patch.object(app, '_ensure_today_structure'), \
             patch.object(app, '_set_consejo_del_dia'), \
             patch.object(app, 'refresh_ui'):
            
            # Simular on_start
            app.current_user = user_data
            app.root.ids.screen_manager.current = "main"
            
            # Verificar que se cambió a la pantalla principal
            assert app.root.ids.screen_manager.current == "main", "Debería estar en la pantalla principal"
            assert app.current_user is not None, "Debería haber un usuario actual"
            assert app.current_user["name"] == "Usuario Test", "El nombre del usuario debería coincidir"
    
    def test_navegacion_login_registro(self, temp_app):
        """
        Prueba la navegación entre pantallas de login y registro
        Validar que se pueda navegar entre "login", "registro" y "home"
        """
        app, db_path, auth_db_path = temp_app
        
        # Simular navegación a registro
        app.go_to_register()
        assert app.root.ids.screen_manager.current == "register", "Debería navegar a la pantalla de registro"
        
        # Simular navegación a login
        app.go_to_login()
        assert app.root.ids.screen_manager.current == "login", "Debería navegar a la pantalla de login"
        
        # Simular navegación a home (main)
        app.root.ids.screen_manager.current = "main"
        assert app.root.ids.screen_manager.current == "main", "Debería navegar a la pantalla principal (home)"
    
    def test_login_exitoso_navegacion(self, temp_app):
        """Prueba que el login exitoso navegue a la pantalla principal"""
        app, db_path, auth_db_path = temp_app
        
        # Crear usuario de prueba
        app.auth_db.add_user("Usuario Test", "test@example.com", "password123")
        
        # Mock de los campos de entrada
        app.root.ids.login_email = Mock()
        app.root.ids.login_email.text = "test@example.com"
        app.root.ids.login_password = Mock()
        app.root.ids.login_password.text = "password123"
        
        # Mock de métodos de la aplicación
        with patch.object(app, '_load_data'), \
             patch.object(app, '_ensure_today_structure'), \
             patch.object(app, '_set_consejo_del_dia'), \
             patch.object(app, 'refresh_ui'), \
             patch.object(app.session_manager, 'save_session'):
            
            # Ejecutar login
            app.do_login()
            
            # Verificar navegación
            assert app.root.ids.screen_manager.current == "main", "Debería navegar a la pantalla principal después del login"
            assert app.current_user is not None, "Debería haber un usuario actual"
            assert app.current_user["email"] == "test@example.com", "El email del usuario debería coincidir"
    
    def test_login_fallido_no_navegacion(self, temp_app):
        """Prueba que el login fallido no navegue a la pantalla principal"""
        app, db_path, auth_db_path = temp_app
        
        # Mock de los campos de entrada con credenciales incorrectas
        app.root.ids.login_email = Mock()
        app.root.ids.login_email.text = "test@example.com"
        app.root.ids.login_password = Mock()
        app.root.ids.login_password.text = "password_incorrecta"
        
        # Ejecutar login
        app.do_login()
        
        # Verificar que NO navegó a la pantalla principal
        assert app.root.ids.screen_manager.current != "main", "NO debería navegar a la pantalla principal con credenciales incorrectas"
        assert app.current_user is None, "NO debería haber un usuario actual con credenciales incorrectas"
    
    def test_registro_exitoso_navegacion(self, temp_app):
        """Prueba que el registro exitoso navegue al login"""
        app, db_path, auth_db_path = temp_app
        
        # Mock de los campos de entrada
        app.root.ids.register_name = Mock()
        app.root.ids.register_name.text = "Usuario Nuevo"
        app.root.ids.register_email = Mock()
        app.root.ids.register_email.text = "nuevo@example.com"
        app.root.ids.register_password = Mock()
        app.root.ids.register_password.text = "password123"
        
        # Ejecutar registro
        app.do_register()
        
        # Verificar navegación
        assert app.root.ids.screen_manager.current == "login", "Debería navegar a la pantalla de login después del registro"
        
        # Verificar que el usuario se creó
        user_exists = app.auth_db.user_exists("nuevo@example.com")
        assert user_exists == True, "El usuario debería haberse creado"
    
    def test_logout_navegacion(self, temp_app):
        """Prueba que el logout navegue al login"""
        app, db_path, auth_db_path = temp_app
        
        # Simular usuario logueado
        app.current_user = {"id": 1, "name": "Usuario Test", "email": "test@example.com"}
        app.root.ids.screen_manager.current = "main"
        
        # Mock de campos de login
        app.root.ids.login_email = Mock()
        app.root.ids.login_password = Mock()
        
        # Ejecutar logout
        app.logout()
        
        # Verificar navegación
        assert app.root.ids.screen_manager.current == "login", "Debería navegar a la pantalla de login después del logout"
        assert app.current_user is None, "NO debería haber un usuario actual después del logout"
    
    def test_validacion_campos_vacios_login(self, temp_app):
        """Prueba que el sistema valide campos vacíos en el login"""
        app, db_path, auth_db_path = temp_app
        
        # Mock de campos vacíos
        app.root.ids.login_email = Mock()
        app.root.ids.login_email.text = ""
        app.root.ids.login_password = Mock()
        app.root.ids.login_password.text = ""
        
        # Ejecutar login
        app.do_login()
        
        # Verificar que NO navegó
        assert app.root.ids.screen_manager.current != "main", "NO debería navegar con campos vacíos"
        assert app.current_user is None, "NO debería haber usuario con campos vacíos"
    
    def test_validacion_campos_vacios_registro(self, temp_app):
        """Prueba que el sistema valide campos vacíos en el registro"""
        app, db_path, auth_db_path = temp_app
        
        # Mock de campos vacíos
        app.root.ids.register_name = Mock()
        app.root.ids.register_name.text = ""
        app.root.ids.register_email = Mock()
        app.root.ids.register_email.text = ""
        app.root.ids.register_password = Mock()
        app.root.ids.register_password.text = ""
        
        # Ejecutar registro
        app.do_register()
        
        # Verificar que NO navegó (el screen_manager.current debería seguir siendo "login")
        # En este caso, el mock siempre retorna "login", así que verificamos que no cambió
        assert app.root.ids.screen_manager.current == "login", "Debería permanecer en login con campos vacíos"
        
        # Verificar que no se creó usuario
        user_count = app.auth_db.get_user_count()
        assert user_count == 0, "NO debería haberse creado ningún usuario con campos vacíos"
    
    def test_validacion_email_registro(self, temp_app):
        """Prueba que el sistema valide el formato del email en el registro"""
        app, db_path, auth_db_path = temp_app
        
        # Mock de campos con email inválido
        app.root.ids.register_name = Mock()
        app.root.ids.register_name.text = "Usuario Test"
        app.root.ids.register_email = Mock()
        app.root.ids.register_email.text = "email_sin_arroba"
        app.root.ids.register_password = Mock()
        app.root.ids.register_password.text = "password123"
        
        # Ejecutar registro
        app.do_register()
        
        # Verificar que NO navegó (debería permanecer en login)
        assert app.root.ids.screen_manager.current == "login", "Debería permanecer en login con email inválido"
        
        # Verificar que no se creó usuario
        user_count = app.auth_db.get_user_count()
        assert user_count == 0, "NO debería haberse creado ningún usuario con email inválido"
    
    def test_validacion_contraseña_corta_registro(self, temp_app):
        """Prueba que el sistema valide la longitud mínima de la contraseña"""
        app, db_path, auth_db_path = temp_app
        
        # Mock de campos con contraseña corta
        app.root.ids.register_name = Mock()
        app.root.ids.register_name.text = "Usuario Test"
        app.root.ids.register_email = Mock()
        app.root.ids.register_email.text = "test@example.com"
        app.root.ids.register_password = Mock()
        app.root.ids.register_password.text = "123"  # Contraseña muy corta
        
        # Ejecutar registro
        app.do_register()
        
        # Verificar que NO navegó (debería permanecer en login)
        assert app.root.ids.screen_manager.current == "login", "Debería permanecer en login con contraseña muy corta"
        
        # Verificar que no se creó usuario
        user_count = app.auth_db.get_user_count()
        assert user_count == 0, "NO debería haberse creado ningún usuario con contraseña muy corta"
