CREATE TABLE IF NOT EXISTS cows (
    id               INTEGER PRIMARY KEY,
    tag              TEXT NOT NULL,
    breed            TEXT,
    lactation_stage  TEXT,            -- early | mid | late | dry
    days_in_milk     INTEGER,
    pregnant         INTEGER DEFAULT 0,
    expected_calving TEXT
);

CREATE TABLE IF NOT EXISTS milk_yield (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    cow_id  INTEGER REFERENCES cows(id),
    date    TEXT NOT NULL,
    litres  REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS health_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cow_id      INTEGER REFERENCES cows(id),
    date        TEXT NOT NULL,
    event_type  TEXT NOT NULL,        -- vaccination | treatment | mastitis_indicator | fever ...
    notes       TEXT
);

CREATE TABLE IF NOT EXISTS feed_logs (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    date         TEXT NOT NULL,
    feed_type    TEXT NOT NULL,
    quantity_kg  REAL,
    protein_pct  REAL,
    notes        TEXT
);

CREATE TABLE IF NOT EXISTS inventory (
    item        TEXT PRIMARY KEY,
    category    TEXT,                 -- feed | medicine | supplement
    quantity    REAL,
    unit        TEXT,
    safe_level  REAL
);

CREATE TABLE IF NOT EXISTS expenses (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    date         TEXT NOT NULL,
    category     TEXT NOT NULL,       -- feed | vet | medicine | labour | other
    amount_inr   REAL NOT NULL,
    description  TEXT
);
