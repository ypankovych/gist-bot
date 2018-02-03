import os
from urllib import parse

import psycopg2


class DataBaseConnect:

    def __init__(self):
        self.parse_object = parse.uses_netloc.append("postgres")
        self.url = parse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
            database=self.url.path[1:],
            user=self.url.username,
            password=self.url.password,
            host=self.url.hostname,
            port=self.url.port
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def new_record(self, message_id, gist_id):
        self.cursor.execute("INSERT INTO main_table (id, gist_id) VALUES (%s, %s)",
                            (message_id, gist_id))

    def select_id(self):
        self.cursor.execute("SELECT id FROM main_table")
        result = self.cursor.fetchall()
        return [x[0] for x in result] if result else []

    def select_gist_id(self, message_id):
        self.cursor.execute("SELECT gist_id FROM main_table WHERE id = %s", (message_id,))
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()

