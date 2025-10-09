# Modelo relacional (SQLite)

## user_profile
- id INTEGER PK CHECK(id=1)
- name TEXT NOT NULL DEFAULT ''
- goal TEXT NOT NULL DEFAULT 'Moverme más'
- created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP

## habit
- key TEXT PK
- title TEXT NOT NULL
- is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0,1))

## day
- day_date TEXT PK (ISO YYYY-MM-DD)

## day_habit
- day_date TEXT NOT NULL FK → day(day_date)
- habit_key TEXT NOT NULL FK → habit(key)
- done INTEGER NOT NULL DEFAULT 0 CHECK(done IN (0,1))
- PK(day_date, habit_key)

**Cardinalidades**
- user_profile 1 ─── N day (conceptual)
- day N ─── N habit (via day_habit)
