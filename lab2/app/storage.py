import os
from datetime import date

import psycopg2
from psycopg2.extras import RealDictCursor


def connect():
    return psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ.get("POSTGRES_PORT", "5432"),
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    )


def _row(row: dict) -> dict:
    checks = row["checks"] or []
    return {
        "id": row["id"],
        "name": row["name"],
        "checks": [day.isoformat() for day in checks],
    }


def list_habits() -> list[dict]:
    with connect() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, name, checks FROM habits ORDER BY id")
            return [_row(row) for row in cur.fetchall()]


def create_habit(name: str) -> dict:
    with connect() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO habits (name) VALUES (%s) RETURNING id, name, checks",
                (name,),
            )
            return _row(cur.fetchone())


def check_habit(habit_id: int, day: date) -> dict | None:
    with connect() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE habits
                SET checks = CASE
                    WHEN %s = ANY(checks) THEN checks
                    ELSE array_append(checks, %s)
                END
                WHERE id = %s
                RETURNING id, name, checks
                """,
                (day, day, habit_id),
            )
            row = cur.fetchone()
    if row is None:
        return None
    return _row(row)
