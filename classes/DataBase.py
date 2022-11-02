import json, sqlite3

class DataBase:
    def __init__(self, path, nameTable):
        self.path = path
        self.connection = sqlite3.connect(self.path, check_same_thread=False)
        self.cursor = self.connection.cursor()

        if "code" in nameTable:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {nameTable}(
                file_type TEXT,
                name TEXT,
                theme TEXT
            )""")

        elif "editor" in nameTable:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {nameTable}(
                                        name TEXT,
                                        theme TEXT
            )""")

        elif "settings" in nameTable:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {nameTable}(
                                        settings TEXT
            )""")

    def command(self, command_request, **kwargs):
        if len(kwargs.keys()) > 0:
            result = [i for i in self.cursor.execute(command_request.format(*list(kwargs.values()))).fetchall()]
        else:
            result = self.cursor.execute(command_request).fetchall()

        return json.loads(str(result[0][0]))

    def close(self):
        self.connection.close()

