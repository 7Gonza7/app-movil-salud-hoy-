PRAGMA foreign_keys = ON;

-- Perfil único de la app
CREATE TABLE IF NOT EXISTS usuario_perfil(
  id INTEGER PRIMARY KEY CHECK (id = 1),
  name TEXT NOT NULL DEFAULT '',
  goal TEXT NOT NULL DEFAULT 'Moverme más',
  created_at DATETIME NOT NULL DEFAULT (datetime('now'))
);

-- Catálogo de hábitos
CREATE TABLE IF NOT EXISTS habito(
  key TEXT PRIMARY KEY,                  -- ej: camina_10
  title TEXT NOT NULL,                   -- ej: Camina 10 minutos
  is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))
);

-- Días (YYYY-MM-DD)
CREATE TABLE IF NOT EXISTS dia(
  day_date TEXT PRIMARY KEY              -- ISO: 2025-10-08
);

-- Estado de hábitos por día (M:N)
CREATE TABLE IF NOT EXISTS habitos_dia(
  day_date TEXT NOT NULL,
  habit_key TEXT NOT NULL,
  done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0,1)),
  PRIMARY KEY (day_date, habit_key),
  FOREIGN KEY (day_date)  REFERENCES dia(day_date)   ON DELETE CASCADE,
  FOREIGN KEY (habit_key) REFERENCES habito(key)      ON DELETE CASCADE
);

-- Índices útiles
CREATE INDEX IF NOT EXISTS idx_habitos_dia_done   ON habitos_dia(done);
CREATE INDEX IF NOT EXISTS idx_habitos_dia_habit  ON habitos_dia(habit_key);

-- Datos base
INSERT OR IGNORE INTO usuario_perfil(id, name, goal) VALUES (1, '', 'Moverme más');

INSERT OR IGNORE INTO habito(key, title, is_active) VALUES
('camina_10','Camina 10 minutos',1),
('estirate_2','Estírate 2 minutos',1),
('respira_1','Respira 1 minuto',1),
('postura_1','Postura recta 1 minuto',1);
