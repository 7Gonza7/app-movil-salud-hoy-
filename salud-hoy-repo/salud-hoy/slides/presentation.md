# Salud Hoy
## Problema y solución
## ERD y Modelo relacional
## Persistencia JSON / SQLite
## Demo y conclusiones

# Salud Hoy
**Equipo**: Nombres — Roles

## Problema
Hábitos saludables simples, medibles y motivadores.

## Solución
App KivyMD con 4 hábitos diarios, consejo del día y sistema de medallas (racha/semana/mes).

## Demo rápida
- Inicio: consejo + checks
- Medallas: chips resumen y grid
- Tips: lista legible
- Perfil: edición en diálogo

## Diseño de datos
- ERD users/day_logs/day_habits/habits
- Relacional: PK/FK, UNIQUE, CHECK 0/1
- Script SQL (SQLite) en `data/schema.sql`

## Implementación
- Python 3.12, Kivy 2.3.0, KivyMD 1.1.1
- Persistencia actual: JSON (`user_data_dir`)
- Opcional: SQLite (script listo)

## Próximos pasos
- Migración JSON → SQLite en app
- Más hábitos configurables
- Sincronización y backup

## Conclusión
Objetivo cumplido según rúbrica: app funcional + diseño de datos + documentación.
