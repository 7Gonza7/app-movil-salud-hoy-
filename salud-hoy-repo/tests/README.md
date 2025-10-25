# Entorno de Pruebas - Salud Hoy

Este directorio contiene todas las pruebas unitarias para el proyecto "Salud Hoy" desarrollado en Python + KivyMD.

## Estructura de Archivos

```
tests/
├── __init__.py              # Paquete de pruebas
├── test_login.py            # Pruebas de autenticación y login
├── test_registro.py         # Pruebas de registro de usuarios
├── test_database.py         # Pruebas de base de datos
├── test_navegacion.py       # Pruebas de navegación y UI
└── README.md               # Este archivo
```

## Archivos de Prueba

### 📄 test_login.py
Prueba el sistema de autenticación:
- ✅ Login con credenciales válidas
- ❌ Login con credenciales incorrectas
- ❌ Login con usuario inexistente
- ❌ Login con campos vacíos
- 🔄 Manejo de mayúsculas/minúsculas en email
- 🧹 Limpieza de espacios en email

### 📄 test_registro.py
Valida el registro de nuevos usuarios:
- ✅ Registro de usuario nuevo exitoso
- ❌ Prevención de email duplicado
- ❌ Validación de campos vacíos
- 🔄 Email case-insensitive
- 🧹 Limpieza de espacios en email
- 👥 Registro de múltiples usuarios

### 📄 test_database.py
Prueba la conexión y operaciones de base de datos:
- 🔗 Conexión a base de datos
- 📋 Verificación de esquema (tabla users)
- 📊 Tablas principales (usuario_perfil, habito, dia, habitos_dia)
- 🌱 Datos iniciales de hábitos
- 👤 Perfil de usuario inicial
- 📅 Operaciones con hábitos del día
- 🔄 Actualización de perfil
- 🔄 Reset de datos

### 📄 test_navegacion.py
Verifica la navegación entre pantallas:
- 🏠 Carga de pantalla principal
- 🔄 Navegación login ↔ registro
- ✅ Login exitoso → pantalla principal
- ❌ Login fallido → permanece en login
- ✅ Registro exitoso → pantalla login
- 🚪 Logout → pantalla login
- ✅ Validación de campos vacíos
- ✅ Validación de formato de email
- ✅ Validación de longitud de contraseña

## Configuración

### pytest.ini
```ini
[pytest]
addopts = -v
testpaths = tests
python_files = test_*.py
```

## Ejecutar Pruebas

### Instalar dependencias
```bash
pip install pytest
```

### Ejecutar todas las pruebas
```bash
pytest
```

### Ejecutar pruebas específicas
```bash
# Solo pruebas de login
pytest tests/test_login.py

# Solo pruebas de base de datos
pytest tests/test_database.py

# Con más detalle
pytest -v tests/
```

### Ejecutar con cobertura
```bash
pip install pytest-cov
pytest --cov=salud-hoy/app tests/
```

## Funciones Probadas

### Autenticación (auth_database.py)
- `check_user()` - Verificación de credenciales
- `user_exists()` - Verificación de existencia de usuario
- `add_user()` - Registro de nuevos usuarios
- `get_user_by_email()` - Obtención de datos por email
- `get_user_count()` - Conteo de usuarios

### Base de Datos (database.py)
- `get_connection()` - Conexión a base de datos
- `get_profile()` - Obtención de perfil
- `update_profile()` - Actualización de perfil
- `get_habits()` - Obtención de hábitos
- `ensure_day_exists()` - Creación de día
- `get_day_habits()` - Hábitos del día
- `set_habit_status()` - Estado de hábito
- `get_completed_count_for_day()` - Conteo de completados
- `reset_all_data()` - Reset de datos

### Sesiones (session_manager.py)
- `save_session()` - Guardar sesión
- `load_session()` - Cargar sesión
- `clear_session()` - Limpiar sesión
- `has_active_session()` - Verificar sesión activa

### Navegación (main.py)
- `do_login()` - Proceso de login
- `do_register()` - Proceso de registro
- `logout()` - Cerrar sesión
- `go_to_login()` - Navegar a login
- `go_to_register()` - Navegar a registro

## Cobertura de Pruebas

Las pruebas cubren:
- ✅ **Autenticación**: Login, registro, validaciones
- ✅ **Base de Datos**: Conexión, esquema, operaciones CRUD
- ✅ **Navegación**: Flujo entre pantallas, validaciones de UI
- ✅ **Sesiones**: Persistencia de sesión
- ✅ **Validaciones**: Campos vacíos, formatos, duplicados

## Notas Técnicas

- Las pruebas usan bases de datos temporales para aislamiento
- Se utilizan mocks para simular componentes de Kivy/KivyMD
- Cada prueba es independiente y puede ejecutarse por separado
- Se incluyen casos de éxito y fallo para cada funcionalidad
- Las pruebas validan tanto el comportamiento esperado como el manejo de errores

## Requisitos

- Python 3.7+
- pytest
- sqlite3 (incluido en Python)
- unittest.mock (incluido en Python)
- tempfile (incluido en Python)
- shutil (incluido en Python)

