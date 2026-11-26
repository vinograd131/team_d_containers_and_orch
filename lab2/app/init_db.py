import os
import time

import psycopg2

SCHEMA = """
CREATE TABLE IF NOT EXISTS habits (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    checks DATE[] NOT NULL DEFAULT '{}'
)
"""


def connect():
    return psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ.get("POSTGRES_PORT", "5432"),
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    )


def main() -> None:
    last_error = None
    for _ in range(30):
        try:
            conn = connect()
            break
        except psycopg2.OperationalError as exc:
            last_error = exc
            time.sleep(1)
    else:
        raise SystemExit(f"postgres is not ready: {last_error}")

    with conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA)
    conn.close()


if __name__ == "__main__":
    main()
