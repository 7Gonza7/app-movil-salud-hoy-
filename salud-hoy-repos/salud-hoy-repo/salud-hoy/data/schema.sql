PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user_profile(
  id INTEGER PRIMARY KEY CHECK (id = 1),
  name TEXT NOT NULL DEFAULT '',
  goal TEXT NOT NULL DEFAULT 'Moverme más',
  created_at DATETIME NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS habit(
  key TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))
);

CREATE TABLE IF NOT EXISTS day(
  day_date TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS day_habit(
  day_date TEXT NOT NULL,
  habit_key TEXT NOT NULL,
  done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0,1)),
  PRIMARY KEY (day_date, habit_key),
  FOREIGN KEY (day_date)  REFERENCES day(day_date)   ON DELETE CASCADE,
  FOREIGN KEY (habit_key) REFERENCES habit(key)      ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_day_habit_done   ON day_habit(done);
CREATE INDEX IF NOT EXISTS idx_day_habit_habit  ON day_habit(habit_key);

INSERT OR IGNORE INTO user_profile(id, name, goal) VALUES (1, '', 'Moverme más');

INSERT OR IGNORE INTO habit(key, title, is_active) VALUES
('camina_10','Camina 10 minutos',1),
('estirate_2','Estírate 2 minutos',1),
('respira_1','Respira 1 minuto',1),
('postura_1','Postura recta 1 minuto',1);
