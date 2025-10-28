import os, sqlite3
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "jobs.sqlite")
DB_PATH = os.path.abspath(DB_PATH)

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS jobs(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  input_path TEXT NOT NULL,
  voice_preset TEXT,
  sample_rate INTEGER DEFAULT 22050,
  bitrate_kbps INTEGER DEFAULT 160,
  status TEXT DEFAULT 'queued',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  started_at DATETIME,
  finished_at DATETIME
);

CREATE TABLE IF NOT EXISTS chapters(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_id INTEGER NOT NULL,
  seq INTEGER NOT NULL,
  text_hash TEXT NOT NULL,
  start_char INTEGER NOT NULL,
  end_char INTEGER NOT NULL,
  status TEXT DEFAULT 'queued',
  progress REAL DEFAULT 0.0,
  artifact_path TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(job_id) REFERENCES jobs(id)
);

CREATE TABLE IF NOT EXISTS metrics(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_id INTEGER,
  chapter_id INTEGER,
  key TEXT,
  value TEXT,
  ts DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

@contextmanager
def connect():
    first = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    if first:
        conn.executescript(SCHEMA)
        conn.commit()
    try:
        yield conn
    finally:
        conn.close()
