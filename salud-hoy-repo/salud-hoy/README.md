# Salud Hoy - Aplicación de Bienestar

**Desarrollado por:** Gonzalo Carvajal

## Descripción

Salud Hoy es una aplicación móvil desarrollada en **KivyMD** que ayuda a los usuarios a mantener hábitos saludables diarios. La aplicación incluye un sistema completo de seguimiento de hábitos, consejos de bienestar, sistema de logros y autenticación de usuarios.

## Características Principales

### Sistema de Autenticación
- **Login seguro** con email y contraseña
- **Registro de nuevos usuarios** con validación
- **Auto-login** para usuarios registrados
- **Gestión de sesiones** con archivos locales
- **Encriptación de contraseñas** con SHA-256

### Seguimiento de Hábitos
- **4 hábitos diarios** predefinidos:
  - Camina 10 minutos
  - Estírate 2 minutos
  - Respira 1 minuto
  - Postura recta 1 minuto
- **Marcado visual** con checkboxes interactivos
- **Persistencia en tiempo real** en base de datos SQLite
- **Contador de días activos** y rachas

### Sistema de Consejos
- **Consejos aleatorios** que cambian diariamente
- **10 consejos diferentes** sobre bienestar y salud
- **Botón "Otro consejo"** para cambiar manualmente
- **Consejos personalizados** basados en el día actual

### Sistema de Logros
- **Medallas y trofeos** por completar hábitos
- **Sistema de badges** por logros específicos
- **Estadísticas detalladas** de progreso
- **Rachas de días consecutivos**

### Perfil de Usuario
- **Información personal** editable
- **Objetivos personalizables**
- **Estadísticas de progreso**
- **Historial de actividades**

### Interfaz Moderna
- **Diseño Material Design 3** con colores emerald green
- **Interfaz responsive** optimizada para móviles
- **Navegación intuitiva** con bottom navigation
- **Animaciones suaves** y transiciones
- **Tema consistente** en toda la aplicación

## Instalación y Ejecución

### Requisitos del Sistema
- Python 3.12+
- Kivy 2.3.0
- KivyMD 1.1.1

### Instalación
```bash
# Instalar dependencias
pip install kivy==2.3.0 kivymd==1.1.1

# Navegar al directorio de la aplicación
cd salud-hoy/app

# Ejecutar la aplicación
python main.py
```

### Primera Ejecución
1. La aplicación se iniciará con la pantalla de login
2. Crear una nueva cuenta haciendo clic en "Crear cuenta"
3. Completar el formulario de registro
4. Iniciar sesión con las credenciales creadas
5. La aplicación recordará la sesión para futuros accesos

## Base de Datos

### SQLite para Datos de la Aplicación
- **Ubicación:** `salud-hoy/data/salud_hoy.db`
- **Creación automática** al ejecutar por primera vez
- **Persistencia en tiempo real** de todos los datos
- **Esquema optimizado** para rendimiento

### SQLite para Autenticación
- **Ubicación:** `salud-hoy/app/data/users.db`
- **Gestión de usuarios** y credenciales
- **Encriptación de contraseñas** con SHA-256
- **Validación de emails únicos**

### Visualizar Datos
```bash
# Ver datos de la aplicación
python app/ver_base_datos.py

# Verificar conexión
python app/verificar_conexion.py

# Ejecutar tests completos
python app/test_complete.py
```

## Estructura del Proyecto

```
salud-hoy/
├── app/
│   ├── main.py                 # Aplicación principal
│   ├── database.py            # Módulo de base de datos
│   ├── auth_database.py       # Gestión de usuarios
│   ├── session_manager.py     # Gestión de sesiones
│   ├── salud_hoy.kv          # Interfaz gráfica
│   ├── test_complete.py      # Suite de testing
│   └── assets/
│       └── logo.png          # Logo de la aplicación
├── data/
│   ├── salud_hoy.db          # Base de datos principal
│   ├── schema.sql            # Esquema de la base de datos
│   └── README_BASE_DE_DATOS.md
├── diagrams/
│   ├── erd.drawio            # Diagrama entidad-relación
│   └── erd.mmd              # Diagrama en Mermaid
└── README.md                # Este archivo
```

## Funcionalidades Técnicas

### Arquitectura
- **Patrón MVC** (Model-View-Controller)
- **Separación de responsabilidades** previa
- **Gestión de estado** con Kivy properties
- **Manejo de errores** robusto

### Seguridad
- **Encriptación de contraseñas** con SHA-256
- **Validación de entrada** en formularios
- **Gestión segura de sesiones**
- **Prevención de inyección SQL**

### Rendimiento
- **Conexiones optimizadas** a base de datos
- **Carga asíncrona** de datos
- **Interfaz responsiva** y fluida
- **Gestión eficiente de memoria**

### Testing
- **Suite de tests completa** con 5 casos de prueba
- **Verificación de imports** y dependencias
- **Tests de base de datos** y operaciones
- **Validación de archivos** y assets
- **Tests de estructura** de la aplicación

## Uso de la Aplicación

### Pantalla de Login
- Ingresar email y contraseña
- Opción de "Crear cuenta" para nuevos usuarios
- Auto-login para usuarios registrados

### Pantalla Principal
- **Consejo del día** con botón para cambiar
- **Lista de hábitos** con checkboxes interactivos
- **Navegación** a otras secciones

### Pantalla de Trofeos
- **Medallas obtenidas** por logros
- **Estadísticas** de progreso
- **Rachas** de días consecutivos

### Pantalla de Tips
- **Consejos adicionales** de bienestar
- **Información educativa** sobre salud

### Pantalla de Perfil
- **Información personal** editable
- **Estadísticas** de uso
- **Botón de cerrar sesión**

## Migración de Datos

Si tienes datos previos en formato JSON, puedes migrarlos:
```bash
python app/migrate_json_to_db.py
```

## Desarrollo y Contribución

### Ejecutar Tests
```bash
python app/test_complete.py
```

### Verificar Estado
```bash
python app/verificar_conexion.py
```

### Estructura de Base de Datos
Ver `data/schema.sql` para el esquema completo de la base de datos.

## Tecnologías Utilizadas

- **Frontend:** Kivy + KivyMD (Python)
- **Base de datos:** SQLite3
- **Autenticación:** SHA-256 + JSON sessions
- **Arquitectura:** MVC (Model-View-Controller)
- **Testing:** Python unittest + custom tests
- **Diseño:** Material Design 3

## Características de Diseño

- **Colores:** Emerald green (#1B5E20) y blanco
- **Tipografía:** Material Design fonts
- **Iconos:** Material Design icons
- **Animaciones:** Transiciones suaves
- **Responsive:** Optimizado para móviles
- **Accesibilidad:** Contraste y tamaños apropiados

## Soporte y Documentación

- **Documentación completa** en archivos .md
- **Tests automatizados** para verificar funcionalidad
- **Código comentado** y bien estructurado
- **Manejo de errores** comprehensivo

## Licencia

Proyecto educativo desarrollado para demostrar habilidades en desarrollo de aplicaciones móviles con Python y KivyMD.

---

**Desarrollado con pasión por el bienestar y la tecnología.**