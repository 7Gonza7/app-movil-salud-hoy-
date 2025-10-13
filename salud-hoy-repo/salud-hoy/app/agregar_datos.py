# -*- coding: utf-8 -*-
"""
Script para agregar más datos a la base de datos
"""

from database import Database
import os
from datetime import date, timedelta

# Conectar a la base de datos
db_path = os.path.join(
    os.path.expanduser('~'),
    'AppData', 'Local', 'SaludHoyApp', 'salud_hoy.db'
)

db = Database(db_path)

print("=" * 60)
print("  AGREGANDO MAS DATOS")
print("=" * 60)

# 1. AGREGAR DATOS DE AYER
ayer = (date.today() - timedelta(days=1)).isoformat()
print(f"\n[*] Agregando habitos de ayer: {ayer}")

db.set_habit_status(ayer, "camina_10", True)
db.set_habit_status(ayer, "respira_1", True)
db.set_habit_status(ayer, "postura_1", True)
print("    [OK] 3 habitos marcados para ayer")

# 2. AGREGAR MÁS DATOS DE HOY
hoy = date.today().isoformat()
print(f"\n[*] Agregando mas habitos de hoy: {hoy}")

db.set_habit_status(hoy, "respira_1", True)
db.set_habit_status(hoy, "postura_1", True)
print("    [OK] 2 habitos adicionales marcados para hoy")

# 3. ACTUALIZAR PERFIL (cambiar objetivo)
print(f"\n[*] Actualizando perfil...")
db.update_profile("Juan Carlos", "Ser más activo cada día")
print("    [OK] Objetivo actualizado")

# Ver resumen
print("\n" + "=" * 60)
print("  RESUMEN")
print("=" * 60)

# Contar totales
completados_hoy = db.get_completed_count_for_day(hoy)
completados_ayer = db.get_completed_count_for_day(ayer)
racha = db.get_streak(threshold=1)

print(f"\nHabitos completados HOY: {completados_hoy}/4")
print(f"Habitos completados AYER: {completados_ayer}/4")
print(f"Racha actual: {racha} dias")

db.close()

print("\n" + "=" * 60)
print("  DATOS AGREGADOS!")
print("=" * 60)
print("\nEjecuta: python ver_base_datos.py")
print("Para ver todos los cambios")




