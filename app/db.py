from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from app import config


def connect() -> psycopg.Connection:
    """Open a new connection; rows come back as dicts."""
    return psycopg.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        row_factory=dict_row,
    )


@contextmanager
def get_conn():
    """Yield a connection; commits on success, rolls back on error, always closes."""
    conn = connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def get_cursor():
    """Yield a cursor inside a transaction managed by get_conn()."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            yield cur
