import mysql.connector


class MysqlDbConnSingleton:
    db_conn = None

    def create_db_conn(self):
        if MysqlDbConnSingleton.db_conn is None:
            MysqlDbConnSingleton.db_conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                db="tourism",
                auth_plugin="mysql_native_password"
            )
        return MysqlDbConnSingleton.db_conn

    def __init__(self):
        self.create_db_conn()

    def add_new_place(self, description="", name=None, nearest_airport="", nearest_bus_terminal="",
                      nearest_railway_station="", state_name="", city_name=""):
        state_id = self.get_state_id_by_name(state_name)
        print("saving place %s for state %s of id %d" % (name, state_name, state_id))
        my_cursor = self.db_conn.cursor()
        id_sql = "SELECT MAX(id) FROM places"
        my_cursor.execute(id_sql)
        last_id = my_cursor.fetchall()[0][0]
        print(last_id)
        if last_id is None:
            last_id = 1
        else:
            last_id += 1
        sql = "INSERT INTO places (id,description,name,nearest_airport,nearest_bus_terminal,nearest_railway_station," \
              "state_id,village_or_city) VALUES (%s,%s, %s,%s,%s,%s,%s,%s)"
        val = (last_id, description, name, nearest_airport, nearest_bus_terminal,
               nearest_railway_station, str(state_id), city_name)
        print("executing query '", sql % val, "'")
        my_cursor.execute(sql, val)
        self.db_conn.commit()
        print(my_cursor.rowcount)

    def get_state_id_by_name(self, name=""):
        cur = self.db_conn.cursor()
        sql_query = "SELECT id FROM states WHERE name='" + name.capitalize() + "'"
        cur.execute(sql_query)
        return cur.fetchall()[0][0]

    def create_state_table(self):
        my_cursor = self.db_conn.cursor()
        sql_check = "SELECT count(*) FROM states"
        my_cursor.execute(sql_check)
        state_records = my_cursor.fetchall()[0]
        if state_records[0] == 0:
            print("no records found inserting dummy state record")
            sql = "INSERT INTO states (id,brief_info,country,description,name, places) VALUES (%s, %s,%s,%s,%s,%s)"
            val = ("1", "some info", "India", "some desc", "Telangana", "10")
            my_cursor.execute(sql, val)
            self.db_conn.commit()
