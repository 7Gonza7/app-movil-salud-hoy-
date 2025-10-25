# -*- coding: utf-8 -*-
"""
Base de datos de autenticación para Salud Hoy
Maneja usuarios, login y registro
"""

import sqlite3
import os
import hashlib


class AuthDatabase:
    """Clase para manejar la autenticación de usuarios"""
    
    def __init__(self, db_path):
        """
        Inicializa la conexión a la base de datos de usuarios
        :param db_path: Ruta completa al archivo de base de datos
        """
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Crea la base de datos y las tablas si no existen"""
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Crear tabla de usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    created_at DATETIME NOT NULL DEFAULT (datetime('now'))
                )
            """)
            
            # Crear índice para búsquedas rápidas por email
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
            """)
            
            conn.commit()
    
    def _hash_password(self, password):
        """
        Hashea la contraseña usando SHA-256
        :param password: Contraseña en texto plano
        :return: Hash de la contraseña
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def get_connection(self):
        """Retorna una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    # ========== REGISTRO ==========
    
    def user_exists(self, email):
        """
        Verifica si un usuario con ese email ya existe
        :param email: Email a verificar
        :return: True si existe, False si no
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email.lower(),))
            count = cursor.fetchone()[0]
            return count > 0
    
    def add_user(self, name, email, password):
        """
        Agrega un nuevo usuario a la base de datos
        :param name: Nombre del usuario
        :param email: Email del usuario
        :param password: Contraseña en texto plano (será hasheada)
        :return: True si se agregó exitosamente, False si ya existe
        """
        email = email.lower().strip()
        
        # Verificar si el usuario ya existe
        if self.user_exists(email):
            return False
        
        # Hash de la contraseña
        password_hash = self._hash_password(password)
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, password_hash)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    # ========== LOGIN ==========
    
    def check_user(self, email, password):
        """
        Verifica las credenciales del usuario
        :param email: Email del usuario
        :param password: Contraseña en texto plano
        :return: Diccionario con datos del usuario si es válido, None si no
        """
        email = email.lower().strip()
        password_hash = self._hash_password(password)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, email FROM users WHERE email = ? AND password = ?",
                (email, password_hash)
            )
            row = cursor.fetchone()
            
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2]
                }
            return None
    
    def get_user_by_email(self, email):
        """
        Obtiene los datos de un usuario por su email
        :param email: Email del usuario
        :return: Diccionario con datos del usuario o None
        """
        email = email.lower().strip()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, email FROM users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2]
                }
            return None
    
    # ========== UTILIDADES ==========
    
    def get_user_count(self):
        """
        Obtiene el número total de usuarios registrados
        :return: Número de usuarios
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            return cursor.fetchone()[0]
    
    def close(self):
        """
        Cierra la conexión (no necesario con context managers)
        """
        pass


