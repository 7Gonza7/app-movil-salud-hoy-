# Plan de implementación y trazabilidad

## Objetivo
Entregar app KivyMD con consejos, 4 hábitos, medallas, perfil y persistencia; más diseño de datos completo y artefactos de entrega.

## Trazabilidad (ERD → Tablas → App)
- **USER_PROFILE** → `user_profile` → Pantalla Perfil (nombre/objetivo).
- **HABIT** → `habit` → 4 hábitos visibles en Inicio.
- **DAY + DAY_HABIT** → `day`, `day_habit` → checks diarios y cómputo de medallas.

## Tareas (estado)
1. UI base KivyMD (Inicio/Medallas/Tips/Perfil) — **OK**
2. Persistencia JSON (local en `user_data_dir`) — **OK**
3. ERD + Relacional — **OK** (`erd.drawio` + `erd.png` + `relational_model.md`)
4. SQLite opcional — **OK** (`data/schema.sql`)
5. Medallas — **OK** (racha, semana, mes + chips resumen)
6. Slides → PDF — **OK** (`slides/presentation.pdf`)
7. README + repo_url — **OK** (completar nombres y URL)

## Riesgos
- Diferencias de versiones Kivy/KivyMD (mitigado fijando versiones).
- Exportación de ERD (resuelto con editable + PNG).

## Cronograma sugerido
- Día 1–2: UI + Persistencia
- Día 3: ERD/Relacional
- Día 4: Slides/README/Repo
