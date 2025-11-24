# -*- coding: utf-8 -*-
import sqlite3
import os
from datetime import date, timedelta


class Database:
    """Clase para manejar todas las operaciones de la base de datos SQLite"""
    
    def __init__(self, db_path):
        """
        Inicializa la conexión a la base de datos
        :param db_path: Ruta completa al archivo de base de datos
        """
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Crea la base de datos y las tablas si no existen"""
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)
        
        # Leer el schema SQL desde data/schema.sql
        # La DB ya está en data/, así que el schema está en el mismo directorio
        schema_path = os.path.join(os.path.dirname(self.db_path), "schema.sql")
        
        with sqlite3.connect(self.db_path) as conn:
            if os.path.exists(schema_path):
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema = f.read()
                conn.executescript(schema)
            else:
                # Schema de respaldo por si no existe el archivo
                self._create_default_schema(conn)
            conn.commit()
    
    def _create_default_schema(self, conn):
        """Crea el schema por defecto si no existe schema.sql"""
        schema = """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS usuario_perfil(
          id INTEGER PRIMARY KEY CHECK (id = 1),
          name TEXT NOT NULL DEFAULT '',
          goal TEXT NOT NULL DEFAULT 'Moverme más',
          created_at DATETIME NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS habito(
          key TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))
        );

        CREATE TABLE IF NOT EXISTS dia(
          day_date TEXT PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS habitos_dia(
          day_date TEXT NOT NULL,
          habit_key TEXT NOT NULL,
          done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0,1)),
          PRIMARY KEY (day_date, habit_key),
          FOREIGN KEY (day_date)  REFERENCES dia(day_date)   ON DELETE CASCADE,
          FOREIGN KEY (habit_key) REFERENCES habito(key)      ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_habitos_dia_done   ON habitos_dia(done);
        CREATE INDEX IF NOT EXISTS idx_habitos_dia_habit  ON habitos_dia(habit_key);

        INSERT OR IGNORE INTO usuario_perfil(id, name, goal) VALUES (1, '', 'Moverme más');

        INSERT OR IGNORE INTO habito(key, title, is_active) VALUES
        ('camina_10','Camina 10 minutos',1),
        ('estirate_2','Estírate 2 minutos',1),
        ('respira_1','Respira 1 minuto',1),
        ('postura_1','Postura recta 1 minuto',1);
        """
        conn.executescript(schema)
    
    def get_connection(self):
        """Retorna una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    # ========== PERFIL ==========
    
    def get_profile(self):
        """Obtiene el perfil del usuario"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, goal FROM usuario_perfil WHERE id = 1")
            row = cursor.fetchone()
            if row:
                return {"name": row[0], "goal": row[1]}
            return {"name": "", "goal": "Moverme más"}
    
    def update_profile(self, name, goal):
        """Actualiza el perfil del usuario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuario_perfil SET name = ?, goal = ? WHERE id = 1",
                (name, goal)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[ERROR] Error al actualizar perfil: {e}")
            raise
    
    # ========== HÁBITOS ==========
    
    def get_habits(self, active_only=True):
        """Obtiene la lista de hábitos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if active_only:
                cursor.execute("SELECT key, title FROM habito WHERE is_active = 1")
            else:
                cursor.execute("SELECT key, title FROM habito")
            return [{"key": row[0], "title": row[1]} for row in cursor.fetchall()]
    
    # ========== DÍAS Y HÁBITOS DIARIOS ==========
    
    def ensure_day_exists(self, day_date):
        """Asegura que existe un registro para el día especificado"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO dia(day_date) VALUES (?)", (day_date,))
            conn.commit()
    
    def get_day_habits(self, day_date):
        """Obtiene el estado de todos los hábitos para un día específico"""
        self.ensure_day_exists(day_date)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.key, COALESCE(dh.done, 0) as done
                FROM habito h
                LEFT JOIN habitos_dia dh ON h.key = dh.habit_key AND dh.day_date = ?
                WHERE h.is_active = 1
            """, (day_date,))
            
            result = {}
            for row in cursor.fetchall():
                result[row[0]] = bool(row[1])
            return result
    
    def set_habit_status(self, day_date, habit_key, done):
        """Establece el estado de un hábito para un día específico"""
        self.ensure_day_exists(day_date)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO habitos_dia(day_date, habit_key, done)
                VALUES (?, ?, ?)
                ON CONFLICT(day_date, habit_key) 
                DO UPDATE SET done = ?
            """, (day_date, habit_key, int(done), int(done)))
            conn.commit()
    
    def get_habits_for_date_range(self, start_date, end_date):
        """Obtiene todos los hábitos completados en un rango de fechas"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT day_date, habit_key, done
                FROM habitos_dia
                WHERE day_date BETWEEN ? AND ? AND done = 1
                ORDER BY day_date
            """, (start_date, end_date))
            
            result = {}
            for row in cursor.fetchall():
                day = row[0]
                if day not in result:
                    result[day] = {}
                result[day][row[1]] = bool(row[2])
            return result
    
    def get_all_days_with_habits(self):
        """Obtiene todos los días que tienen al menos un hábito registrado"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT d.day_date
                FROM dia d
                INNER JOIN habitos_dia dh ON d.day_date = dh.day_date
                ORDER BY d.day_date
            """)
            return [row[0] for row in cursor.fetchall()]
    
    # ========== ESTADÍSTICAS ==========
    
    def get_completed_count_for_day(self, day_date):
        """Cuenta cuántos hábitos se completaron en un día específico"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM habitos_dia
                WHERE day_date = ? AND done = 1
            """, (day_date,))
            row = cursor.fetchone()
            return row[0] if row else 0
    
    def get_streak(self, threshold=1):
        """
        Calcula la racha actual de días consecutivos
        :param threshold: Número mínimo de hábitos completados para contar el día
        """
        today = date.today()
        streak = 0
        current_day = today
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            while True:
                day_str = current_day.isoformat()
                cursor.execute("""
                    SELECT COUNT(*) FROM habitos_dia
                    WHERE day_date = ? AND done = 1
                """, (day_str,))
                row = cursor.fetchone()
                count = row[0] if row else 0
                
                if count >= threshold:
                    streak += 1
                    current_day -= timedelta(days=1)
                else:
                    break
        
        return streak
    
    def get_monthly_active_days(self, year, month):
        """Obtiene el número de días activos en un mes específico"""
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(DISTINCT day_date)
                FROM habitos_dia
                WHERE day_date BETWEEN ? AND ? AND done = 1
            """, (first_day.isoformat(), last_day.isoformat()))
            row = cursor.fetchone()
            return row[0] if row else 0
    
    # ========== UTILIDADES ==========
    
    def reset_all_data(self):
        """Resetea todos los datos (útil para testing o reiniciar la app)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM habitos_dia")
            cursor.execute("DELETE FROM dia")
            cursor.execute("UPDATE usuario_perfil SET name = '', goal = 'Moverme más' WHERE id = 1")
            conn.commit()
    
    def close(self):
        """
        Cierra todas las conexiones activas.
        Nota: Esta clase usa context managers para manejar conexiones,
        por lo que no hay conexiones persistentes que cerrar.
        Este método existe para compatibilidad con la API.
        """
        pass


