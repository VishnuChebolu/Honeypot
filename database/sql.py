from mysql import connector
connection = connector.connect(
    host="localhost",
    user="root",
    password='vishnu'
    )

cursor = connection.cursor()

try:
    cursor.execute(f"create database userlogs;")
    cursor.execute('use userlogs;')
    cursor.execute('create table logs(Time varchar(40), clientIP varchar(30), IP_Version varchar(30), clientPort int, Username varchar(30), Password varchar(30));')
except connector.errors.ProgrammingError as e:
    print(e)
connection.commit()
