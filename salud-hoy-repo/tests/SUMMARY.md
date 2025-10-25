# Resumen de Pruebas - Salud Hoy

## ✅ Archivos de Prueba Creados

### 📄 **test_login.py**
- **Propósito**: Probar login correcto e incorrecto usando `check_user()` y `user_exists()`
- **Funciones probadas**:
  - `test_login_credenciales_validas()` - Verifica que al ingresar credenciales válidas retorne un usuario
  - `test_login_credenciales_incorrectas()` - Verifica que una contraseña incorrecta devuelva `None`
  - `test_login_usuario_inexistente()` - Manejo de usuarios inexistentes
  - `test_login_campos_vacios()` - Validación de campos vacíos
  - `test_login_case_insensitive_email()` - Email case-insensitive
  - `test_login_espacios_en_email()` - Limpieza de espacios

### 📄 **test_registro.py**
- **Propósito**: Usar `add_user()` y `user_exists()` para validar registro
- **Funciones probadas**:
  - `test_registro_usuario_nuevo_exitoso()` - Validar que un usuario nuevo se agregue correctamente
  - `test_registro_email_duplicado()` - Validar que el sistema bloquee el registro si el correo ya existe
  - `test_registro_campos_vacios()` - Validación de campos vacíos
  - `test_registro_email_case_insensitive()` - Email case-insensitive
  - `test_registro_espacios_en_email()` - Limpieza de espacios
  - `test_registro_multiple_usuarios_diferentes()` - Registro de múltiples usuarios

### 📄 **test_database.py**
- **Propósito**: Probar que `connect_db()` cree el archivo `salud_hoy.db` en `data/`
- **Funciones probadas**:
  - `test_conexion_base_datos()` - Simula connect_db() creando el archivo salud_hoy.db
  - `test_esquema_tabla_users()` - Comprueba que la tabla users exista tras la conexión
  - `test_conexion_sin_errores()` - Valida que la conexión no arroje errores
  - `test_esquema_tablas_principales()` - Tablas principales de la aplicación
  - `test_datos_iniciales_habitos()` - Datos iniciales de hábitos
  - `test_perfil_usuario_inicial()` - Perfil de usuario inicial
  - `test_operaciones_habitos_dia()` - Operaciones con hábitos del día
  - `test_actualizacion_perfil()` - Actualización de perfil
  - `test_reset_datos()` - Reset de datos

### 📄 **test_navegacion.py**
- **Propósito**: Simular cambio de pantallas del `ScreenManager` de `main.py`
- **Funciones probadas**:
  - `test_carga_pantalla_principal()` - Simular cambio de pantallas del ScreenManager de main.py
  - `test_navegacion_login_registro()` - Validar que se pueda navegar entre "login", "registro" y "home"
  - `test_login_exitoso_navegacion()` - Login exitoso navegue a la pantalla principal
  - `test_login_fallido_no_navegacion()` - Login fallido no navegue
  - `test_registro_exitoso_navegacion()` - Registro exitoso navegue al login
  - `test_logout_navegacion()` - Logout navegue al login
  - `test_validacion_campos_vacios_login()` - Validación de campos vacíos
  - `test_validacion_campos_vacios_registro()` - Validación de campos vacíos
  - `test_validacion_email_registro()` - Validación de formato de email
  - `test_validacion_contraseña_corta_registro()` - Validación de longitud de contraseña

## 🧰 Configuración

### **pytest.ini**
```ini
[pytest]
addopts = -v
testpaths = tests
python_files = test_*.py
```

### **Imports Actualizados**
Todos los archivos comienzan con:
```python
import pytest
from app.database import *
```

## 🚀 Cómo Ejecutar

### Opción 1: Usando pytest directamente
```bash
# Instalar pytest
pip install pytest

# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas específicas
pytest tests/test_login.py
pytest tests/test_database.py
```

### Opción 2: Usando el script runner
```bash
python run_tests.py
```

## 📊 Cobertura de Pruebas

- ✅ **Autenticación**: `check_user()`, `user_exists()`, `add_user()`
- ✅ **Base de Datos**: Conexión, esquema, operaciones CRUD
- ✅ **Navegación**: Flujo entre pantallas, validaciones de UI
- ✅ **Validaciones**: Campos vacíos, formatos, duplicados
- ✅ **Manejo de Errores**: Casos de éxito y fallo

## 📝 Documentación Interna

Cada test incluye:
- **Comentarios descriptivos** explicando qué se está probando
- **Asserts claros** con mensajes de error descriptivos
- **Docstrings** detallando el propósito de cada función
- **Validación específica** de los requerimientos del usuario

## 🎯 Cumplimiento de Requerimientos

✅ **test_login.py**: Probar login correcto e incorrecto usando `check_user()` y `user_exists()`  
✅ **test_registro.py**: Usar `add_user()` y `user_exists()` para validar registro  
✅ **test_database.py**: Probar que `connect_db()` cree el archivo `salud_hoy.db` en `data/`  
✅ **test_navegacion.py**: Simular cambio de pantallas del `ScreenManager` de `main.py`  
✅ **Imports**: Todos los archivos comienzan con `import pytest` y `from app.database import *`  
✅ **Documentación**: Comentarios descriptivos y asserts claros en cada test  
✅ **Validación**: Al menos 2-3 funciones con `assert` que validen comportamiento esperado

