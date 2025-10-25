# 📊 Base de Datos SQLite - Salud Hoy

## 📁 Archivo: `salud_hoy.db`

Esta es una copia de la base de datos de la aplicación, lista para ser visualizada en VS Code.

---

## 🔍 Cómo Ver las Tablas en VS Code

### Opción 1: Usando el Buscador Rápido (Ctrl+P)

1. Presiona `Ctrl + P`
2. Escribe: `salud_hoy.db`
3. Presiona Enter
4. La base de datos se abrirá con la extensión SQLite Viewer

### Opción 2: Desde el Explorador de Archivos

1. Ve a la carpeta `data/` en el explorador
2. Haz clic derecho en `salud_hoy.db`
3. Selecciona **"Open Database"**

### Opción 3: Paleta de Comandos

1. Presiona `Ctrl + Shift + P`
2. Escribe: `SQLite: Open Database`
3. Selecciona el archivo `salud_hoy.db`

---

## 📋 Tablas Disponibles

La base de datos contiene las siguientes tablas:

### 1. `usuario_perfil`
- **Columnas:** `id`, `name`, `goal`, `created_at`
- **Descripción:** Información del perfil del usuario

### 2. `habito`
- **Columnas:** `key`, `title`, `is_active`
- **Descripción:** Lista de hábitos disponibles en la app

### 3. `dia`
- **Columnas:** `day_date`
- **Descripción:** Registro de días con actividad

### 4. `habitos_dia`
- **Columnas:** `day_date`, `habit_key`, `done`
- **Descripción:** Estado de cada hábito por día

---

## 🔄 Actualizar la Base de Datos

La base de datos real de la app está en:
```
C:\Users\carva\AppData\Local\SaludHoyApp\salud_hoy.db
```

Para actualizar la copia en el proyecto, ejecuta:

```bash
python app/copiar_db_al_proyecto.py
```

Esto copiará la versión más reciente de AppData al proyecto.

---

## 🛠️ Extensiones Recomendadas

Para visualizar la base de datos, asegúrate de tener instaladas:

- **SQLite Viewer** (qwtel.sqlite-viewer) ✅
- **SQLite** (alexcvzz.vscode-sqlite) ✅

---

## 📝 Consultas SQL de Ejemplo

Si usas la extensión SQLite, puedes ejecutar consultas SQL directamente:

### Ver todos los hábitos
```sql
SELECT * FROM habito WHERE is_active = 1;
```

### Ver perfil del usuario
```sql
SELECT name, goal FROM usuario_perfil WHERE id = 1;
```

### Ver hábitos completados hoy
```sql
SELECT h.title, hd.done 
FROM habito h
LEFT JOIN habitos_dia hd ON h.key = hd.habit_key
WHERE hd.day_date = date('now')
ORDER BY h.title;
```

### Ver racha de días activos
```sql
SELECT day_date, COUNT(*) as habitos_completados
FROM habitos_dia
WHERE done = 1
GROUP BY day_date
ORDER BY day_date DESC;
```

---

## ⚠️ Importante

- Esta es una **copia** de la base de datos
- Los cambios aquí **NO afectan** la app
- Para ver datos actualizados, ejecuta `copiar_db_al_proyecto.py` nuevamente
- La base de datos real está en AppData

---

## 🎯 Uso Típico

1. **Ejecuta la app** y usa algunas funciones
2. **Copia la DB** con `python app/copiar_db_al_proyecto.py`
3. **Abre en VS Code** con `Ctrl+P` → `salud_hoy.db`
4. **Explora las tablas** usando SQLite Viewer
5. **Ejecuta consultas** para analizar los datos

---

## 📊 Diagrama ER

Para ver el diagrama de la base de datos, consulta:
- `diagrams/erd.drawio` - Diagrama visual
- `diagrams/relational_model.md` - Modelo relacional detallado












