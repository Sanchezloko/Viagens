import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_id TEXT NOT NULL,
    origem TEXT NOT NULL,
    destino TEXT NOT NULL,
    data_ida TEXT NOT NULL,
    data_volta TEXT,
    pax INTEGER NOT NULL,
    classe TEXT NOT NULL,
    preco REAL NOT NULL,
    moeda TEXT NOT NULL,
    cia TEXT,
    link TEXT,
    fonte TEXT,
    coletado_em TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_price_history_search
    ON price_history(search_id, coletado_em);

CREATE TABLE IF NOT EXISTS alerts_sent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_id TEXT NOT NULL,
    preco REAL NOT NULL,
    enviado_em TEXT NOT NULL,
    payload TEXT
);

CREATE INDEX IF NOT EXISTS idx_alerts_search
    ON alerts_sent(search_id, enviado_em);
"""


@contextmanager
def conn():
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(config.DB_PATH)
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    finally:
        c.close()


def init():
    with conn() as c:
        c.executescript(SCHEMA)
        try:
            c.execute("ALTER TABLE price_history ADD COLUMN fonte TEXT")
        except Exception:
            pass  # coluna já existe


def insert_price(search_id, origem, destino, data_ida, data_volta,
                 pax, classe, preco, moeda, cia, link, fonte=None):
    with conn() as c:
        c.execute(
            """INSERT INTO price_history
               (search_id, origem, destino, data_ida, data_volta, pax, classe,
                preco, moeda, cia, link, fonte, coletado_em)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (search_id, origem, destino, data_ida, data_volta, pax, classe,
             preco, moeda, cia, link, fonte, datetime.now(timezone.utc).isoformat()),
        )


def has_travelpayouts_today(search_id):
    today = datetime.now(timezone.utc).date().isoformat()
    with conn() as c:
        row = c.execute(
            """SELECT 1 FROM price_history
               WHERE search_id = ? AND fonte = 'travelpayouts' AND coletado_em >= ?
               LIMIT 1""",
            (search_id, today),
        ).fetchone()
        return row is not None


def recent_prices(search_id, days=None):
    days = days or config.HISTORY_DAYS
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    with conn() as c:
        rows = c.execute(
            """SELECT preco FROM price_history
               WHERE search_id = ? AND coletado_em >= ?
               ORDER BY coletado_em ASC""",
            (search_id, cutoff),
        ).fetchall()
        return [r["preco"] for r in rows]


def last_alert(search_id):
    with conn() as c:
        row = c.execute(
            """SELECT enviado_em, preco FROM alerts_sent
               WHERE search_id = ?
               ORDER BY enviado_em DESC LIMIT 1""",
            (search_id,),
        ).fetchone()
        return dict(row) if row else None


def insert_alert(search_id, preco, payload):
    with conn() as c:
        c.execute(
            """INSERT INTO alerts_sent (search_id, preco, enviado_em, payload)
               VALUES (?,?,?,?)""",
            (search_id, preco,
             datetime.now(timezone.utc).isoformat(), payload),
        )


def prune_old_history(days=None):
    """Mantém o DB enxuto pra não inflar o repo."""
    days = days or max(config.HISTORY_DAYS, 180)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    with conn() as c:
        c.execute("DELETE FROM price_history WHERE coletado_em < ?", (cutoff,))
        c.execute("DELETE FROM alerts_sent WHERE enviado_em < ?", (cutoff,))
