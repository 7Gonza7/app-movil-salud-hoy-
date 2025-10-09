# Salud Hoy
App móvil (KivyMD) para hábitos saludables con **consejo del día**, **4 hábitos diarios** y **sistema de medallas** (racha/semana/mes).
Incluye todo lo exigido por la rúbrica: README, ERD editable + imagen, modelo relacional, schema SQL opcional, código de app, plan de implementación, slides y repo_url.

## Integrantes y roles
- (Completar) – Desarrollador/a KivyMD, UI/UX
- (Completar) – Diseño de datos (ERD/Modelo Relacional), QA
- (Completar) – Documentación y presentación

## Requisitos
- Python 3.12+
- Kivy 2.3.0
- KivyMD 1.1.1

## Ejecutar
```bash
pip install kivy==2.3.0 kivymd==1.1.1
python salud-hoy/app/main.py
```

## Estructura
- `salud-hoy/app/` código KivyMD (UI responsive, tema verde, texto negro, medallas, perfil).
- `salud-hoy/diagrams/` ERD editable (`erd.drawio`) + imagen (`erd.png`) + modelo relacional (`relational_model.md`).
- `salud-hoy/data/` `schema.sql` (SQLite opcional) listo.
- `salud-hoy/slides/` `presentation.pdf` para exponer.
- `implementation_plan.md` plan de trabajo y trazabilidad.
- `repo_url.txt` URL del repo.

## Persistencia
La app actualmente usa **JSON local** en `user_data_dir` para máxima portabilidad. Se incluye `data/schema.sql` por si quieres migrar a SQLite.
