import os
import io
import random
import csv
import psycopg2
from psycopg2.extensions import cursor as t_cursor
from psycopg2.extensions import connection as t_conn
from datetime import datetime, timedelta

from config import DB_CONFIG, APP_CONFIG


def create_table(cursor: t_cursor):
    cursor.execute("""
        DROP TABLE IF EXISTS sensor_status;
        CREATE TABLE sensor_status (
            id BIGSERIAL PRIMARY KEY,
            channel_id INTEGER NOT NULL,
            event_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            value DOUBLE PRECISION NOT NULL,
            alarm_flag SMALLINT DEFAULT 0 NOT NULL
        );    
    """)


def insert_data_table(cursor: t_cursor):
    begin_time = datetime(2026, 11, 1, 0, 0, 0)
    buffer = io.StringIO()

    for i in range(APP_CONFIG["count_records"]):
        channel_id = random.randint(1, 50)
        event_time = begin_time + timedelta(seconds=i)
        value = random.uniform(0.0, 10.0)
        buffer.write(f"{channel_id}\t{event_time}\t{value}\n")

    buffer.seek(0)

    cursor.copy_expert(
        """
        COPY sensor_status (channel_id, event_time, value)
        FROM STDIN WITH DELIMITER E'\t'
        """,
        buffer,
    )


def read_data_table(cursor: t_cursor):
    cursor.execute("SELECT COUNT(*) FROM sensor_status WHERE value < 7.0;")
    count_records = cursor.fetchone()[0]
    print("-----")
    print(f"Count records (< 7.0): `{count_records}`")
    print("-----")

    cursor.execute(
        """SELECT channel_id, event_time, value
        FROM sensor_status
        WHERE value < 7.0
        LIMIT 10;
        """
    )

    for row in cursor.fetchall():
        print(f"Channel: {row[0]}, Time: {row[1]}, Value: {row[2]}")


def update_data_table(cursor: t_cursor):
    cursor.execute("""
        UPDATE sensor_status
        SET alarm_flag = 1
        WHERE value >= 3.0 AND value < 7.0;             
    """)
    updated_1 = cursor.rowcount

    cursor.execute("""
        UPDATE sensor_status
        SET alarm_flag = 2
        WHERE value >= 4.0 AND value < 7.0;    
    """)
    updated_2 = cursor.rowcount

    print("-----")
    print(f"Updated `{updated_1}` records: alarm_flag = 1")
    print(f"Updated `{updated_2}` records: alarm_flag = 2")
    print("-----")


def export_to_csv(cursor: t_cursor, flag: int, filename: str):
    cursor.execute(
        """
        SELECT id, channel_id, event_time, value, alarm_flag
        FROM sensor_status
        WHERE alarm_flag = %s;              
    """,
        (flag,),
    )

    path_to_file = os.path.join(APP_CONFIG["res_dir"], filename)

    with open(path_to_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "channel_id", "event_time", "value", "alarm_flag"])
        writer.writerows(cursor.fetchall())
    print(f"> File `{filename}` written")


def main():
    try:
        print("-----")
        print(f"> Connecting database `{DB_CONFIG['dbname']}`")
        conn: t_conn = psycopg2.connect(**DB_CONFIG)
        print("> SUCCESS")

        conn.autocommit = False
        cursor = conn.cursor()

        create_table(cursor)

        print("> Inserting data in table")
        insert_data_table(cursor)
        conn.commit()
        print("> SUCCESS")

        read_data_table(cursor)
        update_data_table(cursor)
        conn.commit()

        os.makedirs(APP_CONFIG["res_dir"], exist_ok=True)
        export_to_csv(cursor, 1, APP_CONFIG["warn_file"])
        export_to_csv(cursor, 2, APP_CONFIG["alarm_file"])

    except Exception as err:
        print("!!!!!")
        print(f"Error: {err}")
        print("!!!!!")
        if "conn" in locals():
            conn.rollback()

    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
            print("-----")
            print("Connection with database is closed")
            print("-----")


if __name__ == "__main__":
    main()
