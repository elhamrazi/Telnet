import mysql.connector

db_connection = mysql.connector.connect(host="localhost",
                                        user="root",
                                        password="",
                                        database="telnetdb")
print("successfully connected to mysql database")
print(db_connection)
mycursor = db_connection.cursor()


def insert_data(cursor, port, command, cmd_time, cmd_date):
    sql = "INSERT INTO history (port, command, cmd_time, cmd_date) VALUES  (%s, %s, %s, %s)"
    val = (port, command, cmd_time, cmd_date)
    cursor.execute(sql, val)
    db_connection.commit()
    print(cursor.rowcount, "record inserted")


def print_history(cursor):
    cursor.execute("SELECT * FROM history")

    # fetch all the matching rows
    result = cursor.fetchall()

    # loop through the rows
    s = ""
    for row in result:
        # print(row)
        s += "Port: " + str(row[0]) + "\t" + "Command: " + str(row[1]) + "\t" + "Time: " + str(row[2]) + "\t" + "Date: " \
             + str(row[3]) + "\n"
    print(s)
    return s


# print_history(mycursor)


