# -*- coding: utf-8 -*-
"""
Script para simular datos en la base de datos
(Como si hubieras marcado hábitos en la app)
"""

from app.database import Database
import os
from datetime import date

# Conectar a la base de datos
db_path = os.path.join(
    os.path.expanduser('~'),
    'AppData', 'Local', 'SaludHoyApp', 'salud_hoy.db'
)

db = Database(db_path)

print("=" * 60)
print("  SIMULANDO DATOS DE EJEMPLO")
print("=" * 60)

# Marcar hábitos de HOY
hoy = date.today().isoformat()
print(f"\n[*] Marcando habitos del dia: {hoy}")

db.set_habit_status(hoy, "camina_10", True)
print("    [OK] Camina 10 minutos - Marcado")

db.set_habit_status(hoy, "estirate_2", True)
print("    [OK] Estirate 2 minutos - Marcado")

# Actualizar perfil
print("\n[*] Actualizando perfil...")
db.update_profile("Juan Carlos", "Mejorar mi salud")
print("    [OK] Perfil actualizado")

db.close()

print("\n" + "=" * 60)
print("  DATOS SIMULADOS!")
print("=" * 60)
print("\nAhora ejecuta: python ver_base_datos.py")
print("Veras que las tablas tienen datos!")




