# -*- coding: utf-8 -*-
"""
Gestión de sesiones para Salud Hoy
Maneja la persistencia de sesión entre ejecuciones
"""

import json
import os


class SessionManager:
    """Clase para manejar la sesión del usuario"""
    
    def __init__(self, session_file="session.json"):
        """
        Inicializa el gestor de sesiones
        :param session_file: Nombre del archivo de sesión
        """
        # Ruta al archivo de sesión en el directorio de la app
        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.session_path = os.path.join(app_dir, session_file)
    
    def save_session(self, user_data):
        """
        Guarda la sesión del usuario en un archivo JSON
        :param user_data: Diccionario con datos del usuario (email, name, id)
        """
        try:
            with open(self.session_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[ERROR] Error al guardar sesión: {e}")
            return False
    
    def load_session(self):
        """
        Carga la sesión guardada del archivo JSON
        :return: Diccionario con datos del usuario o None si no hay sesión
        """
        if not os.path.exists(self.session_path):
            return None
        
        try:
            with open(self.session_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Error al cargar sesión: {e}")
            return None
    
    def clear_session(self):
        """
        Elimina la sesión guardada (cierre de sesión)
        """
        if os.path.exists(self.session_path):
            try:
                os.remove(self.session_path)
                return True
            except Exception as e:
                print(f"[ERROR] Error al eliminar sesión: {e}")
                return False
        return True
    
    def has_active_session(self):
        """
        Verifica si hay una sesión activa
        :return: True si hay sesión activa, False si no
        """
        return os.path.exists(self.session_path) and self.load_session() is not None


