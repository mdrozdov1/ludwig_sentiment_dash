import os
import config
import psycopg2 as ps
from flask import jsonify

try:
    with ps.connect(database = config.POSTGRES_DB, user = config.POSTGRES_USER, 
    password = config.POSTGRES_PASSWORD, host = config.POSTGRES_HOST, port = config.POSTGRES_PORT) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                review_label INTEGER,
                description VARCHAR(400),
                date DATE
                );
            """)
finally:
    conn.close()

def add_record(review_label, description, date):
    try:
        with ps.connect(database = config.POSTGRES_DB, user = config.POSTGRES_USER,
        password = config.POSTGRES_PASSWORD, host = config.POSTGRES_HOST, port = config.POSTGRES_PORT) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO reviews (review_label, description, date) VALUES (%s, %s, %s)
                    """,
                    (review_label, description, date)
                    )
    finally:
        return jsonify(conn.close())