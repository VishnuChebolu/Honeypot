from mysql import connector

connection = connector.connect(
    host="localhost",
    user="root",
    password='vishnu',
    database='userlogs'
    )


def insert(ip, version, port, username, password):
    import datetime
    cursor = connection.cursor()
    time = datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S")
    time = str(time)
    try:
        command = f'insert into logs(Time, clientIP, IP_Version, clientPort, Username, Password) values ("{time}", "{ip}", "{version}", {port}, "{username}", "{password}");'
        # print(command)
        cursor.execute(f'{command}')
    except connector.errors.ProgrammingError as e:
        print(e)
    connection.commit()