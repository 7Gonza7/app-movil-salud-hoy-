Salud Hoy — Persistencia de Datos
Equipo (edita): Integrantes y roles.

Descripción
App en KivyMD con checklist diario, consejos, trofeos/medallas y perfil. ** Ahora con persistencia de datos usando SQLite **

Ejecutar
pip install kivy==2.3.0 kivymd==1.1.1
python app/main.py
Base de Datos SQLite
La aplicación ahora utiliza SQLite para almacenar todos los datos de forma persistente:

Perfil de usuario (nombre, objetivo)
Catálogo de hábitos
Seguimiento diario de hábitos completados
Historial completo para estadísticas y medallas
Ubicación de la base de datos
El archivo salud_hoy.db se guarda directamente en el proyecto:

Ubicación: salud-hoy/data/salud_hoy.db
Se crea automáticamente al ejecutar la app por primera vez
Todos los cambios se guardan en tiempo real en este archivo
Visualizar la Base de Datos
Para ver las tablas y datos:

En VS Code (recomendado):

Presiona Ctrl + P
Escribe: salud_hoy.db
O navega a data/salud_hoy.db y haz clic derecho → "Open Database"
En la terminal:

python app/ver_base_datos.py
Verificar conexión:

python app/verificar_conexion.py
Más información: Ver ARCHIVOS_COMPLETOS_LISTOS.md

Migrar datos antiguos (JSON → SQLite)
Si tenías datos previos en formato JSON, puedes migrarlos:

python app/migrate_json_to_db.py
Estructura
app/ código Kivy/KivyMD
main.py - Aplicación principal (conectada a SQLite)
database.py - Módulo de base de datos SQLite
salud_hoy.kv - Interfaz gráfica
ver_base_datos.py - Ver datos en terminal
verificar_conexion.py - Verificar estado de la DB
migrate_json_to_db.py - Script de migración (opcional)
data/
salud_hoy.db - BASE DE DATOS (todos los datos se guardan aquí)
schema.sql - Schema de la base de datos SQLite
README_BASE_DE_DATOS.md - Guía para ver la DB
diagrams/ - ERD y modelo relacional
ARCHIVOS_COMPLETOS_LISTOS.md - Documentación completa de la conexión
implementation_plan.md - Plan de implementación
slides/presentation.md - Presentación (exporta a PDF)
Características
Seguimiento diario de 4 hábitos saludables
Consejos de salud rotatorios
Sistema de medallas y logros
Perfil personalizable
Estadísticas (racha, días activos)
Persistencia con SQLite
Interfaz optimizada (400x700px, sin desbordamiento)
Integrantes y roles
Gonzalo Carvajal – Desarrollador/a KivyMD, UI/UX
Gonzalo Carvajal – Diseño de datos (ERD/Modelo Relacional), QA
Gonzalo Carvajal – Documentación y presentación
Requisitos
Python 3.12+
Kivy 2.3.0
KivyMD 1.1.1
pip install kivy==2.3.0 kivymd==1.1.1
python salud-hoy/app/main.py
Tecnologías
Frontend: Kivy + KivyMD (Python)
Base de datos: SQLite3
Arquitectura: MVC (Model-View-Controller)
