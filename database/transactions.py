# encoding: utf-8

import logging
import sqlite3
import datetime

class TransactionsEngine():
    def __init__(self, db_name):
        self.db_name = db_name

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS last_travel (url text primary key)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS travels (url text primary key, date text, 
                            timestamp datetime DEFAULT CURRENT_TIMESTAMP, fetched integer DEFAULT 0)''')

        conn.commit()

        self.disconnect(conn)

    def connect(self):
        conn = sqlite3.connect('files/{0}'.format(self.db_name))

        return conn


    def disconnect(self, conn):
        conn.close()

    def get_last_to_check(self):
        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM last_travel""")

        travel = cursor.fetchone()

        self.disconnect(conn)

        if travel is None:
            return travel
        else:
            return travel[0]


    def update_last_to_check(self, last_url):
        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""SELECT COUNT(*) from last_travel""")

        count = cursor.fetchone()[0]

        if count <= 0:
            cursor.execute("""INSERT INTO last_travel VALUES (?)""", (last_url,))
        else:
            cursor.execute("""UPDATE last_travel SET url = ?""", (last_url,))

        conn.commit()

        self.disconnect(conn)


    def insert_travel(self, url, date):
        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""INSERT INTO travels VALUES (?, ?, ?, ?)""",
                    (url, date, datetime.datetime.now(), 0))

        conn.commit()

        self.disconnect(conn)


    def set_travel_fetched(self, url):
        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """UPDATE travels SET fetched = 1 WHERE url = ?""", (url,))

        conn.commit()

        self.disconnect(conn)


    def get_unfetched_travels(self):
        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM travels WHERE fetched = 0 ORDER BY timestamp DESC""")

        travels = cursor.fetchall()

        self.disconnect(conn)

        return travels
