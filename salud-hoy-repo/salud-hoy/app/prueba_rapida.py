# -*- coding: utf-8 -*-
"""Prueba rápida de la base de datos"""

from database import Database
from datetime import date
import os
import tempfile

# Conectar a la base de datos (en directorio temporal)
temp_dir = tempfile.gettempdir()
db_path = os.path.join(temp_dir, "prueba_temporal.db")
db = Database(db_path)

print("=" * 60)
print("PRUEBA RÁPIDA DE BASE DE DATOS")
print("=" * 60)

# 1. Ver perfil
print("\n1. PERFIL:")
perfil = db.get_profile()
print(f"   Nombre: {perfil['name'] or '(vacío)'}")
print(f"   Objetivo: {perfil['goal']}")

# 2. Actualizar perfil
print("\n2. ACTUALIZANDO PERFIL:")
db.update_profile("Mi Nombre", "Estar más saludable")
perfil = db.get_profile()
print(f"   Nuevo nombre: {perfil['name']}")
print(f"   Nuevo objetivo: {perfil['goal']}")

# 3. Ver hábitos
print("\n3. HÁBITOS DISPONIBLES:")
habitos = db.get_habits()
for h in habitos:
    print(f"   - {h['title']} ({h['key']})")

# 4. Marcar hábitos de hoy
print("\n4. MARCANDO HÁBITOS DE HOY:")
hoy = date.today().isoformat()
db.set_habit_status(hoy, "camina_10", True)
db.set_habit_status(hoy, "estirate_2", True)
print(f"   Fecha: {hoy}")
print("   Marcados: Caminar y Estirar")

# 5. Ver hábitos de hoy
print("\n5. HÁBITOS DE HOY:")
habitos_hoy = db.get_day_habits(hoy)
for key, done in habitos_hoy.items():
    estado = "[OK]" if done else "[ ]"
    print(f"   {estado} {key}")

# 6. Contar completados
completados = db.get_completed_count_for_day(hoy)
print(f"\n6. COMPLETADOS HOY: {completados}/4")

# 7. Ver racha
racha = db.get_streak(threshold=1)
print(f"\n7. RACHA ACTUAL: {racha} día(s)")

# 8. Cerrar
db.close()
print("\n" + "=" * 60)
print("[OK] PRUEBA COMPLETADA")
print("=" * 60)

# Limpiar archivo temporal
try:
    os.remove(db_path)
    print("\n[*] Archivo temporal eliminado")
except:
    pass

