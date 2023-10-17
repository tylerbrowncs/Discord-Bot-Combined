import sqlite3, config

class Database():
    def __init__(self):
        self.connection = sqlite3.connect(config.database_file) # Replace with a remote connection in future.
        self.db = self.connection.cursor()

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS servers(
            id INTEGER PRIMARY KEY,
            dj_role TEXT,
            admin_role TEXT,
            prefix TEXT
        )""")

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            messages INTEGER,
            commands INTEGER,
            attachments INTEGER,
            birthday STRING
        )""")

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS timers(
            id INTEGER PRIMARY KEY,
            timer_name TEXT,
            count_to TEXT,
            author_id TEXT,
            time_elapsed INTEGER
        )
        """)



        self.connection.commit()


    def add_server(self, id):

        if id is not None:

            self.db.execute(f"""
            INSERT OR IGNORE INTO servers (id, dj_role, admin_role, prefix) VALUES ({id}, 'DJ', 'Admin', '-')
        
            """)

        self.connection.commit()

    def add_user(self, id):
         if id is not None:

            self.db.execute(f"""
            INSERT OR IGNORE INTO users (id, messages, commands, attachments, birthday) VALUES ({id}, 0, 0, 0, '')
        
            """)

    def add_timer(self, id, authorid, count_date, name):

        self.db.execute(f"""
        INSERT OR IGNORE INTO timers (id,timer_name,count_to,author_id,time_elapsed) VALUES ({id}, '{authorid}', '{count_date}', '{name}', 0)
        """)

    def get(self, table, id):
        self.db.execute(f"""
        SELECT * FROM {table} WHERE id={id}
        """)
        results = self.db.fetchall()[0]

        self.db.execute(f"""PRAGMA table_info({table})""")
        keys = self.db.fetchall()

        data = {}

        for i in range(0, len(results)):
            data[keys[i][1]] = results[i]


        return data

    def leaderboard(self, table, order_by):
        self.db.execute(f"""
        SELECT * FROM {table} ORDER BY {order_by} DESC LIMIT 10
        """)

        return self.db.fetchall()

    def change(self, table, id, key, arg):

        self.db.execute(f"""
        UPDATE {table} SET {key} = '{arg}' WHERE id = {id}""")

    def saveAll(self):
        self.connection.commit()



