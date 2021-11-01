def insert(ip, version, port, username, password):
    # print('called')
    from mysql import connector
    import pytz

    connection = connector.connect(
        host="localhost",
        user="root",
        password='vishnu',
        database='userlogs'
        )
    import datetime
    cursor = connection.cursor()
    time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%a, %d %B %Y %H:%M:%S")
    time = str(time)
    try:
        command = f'insert into logs(Time, clientIP, IP_Version, clientPort, Username, Password) values ("{time}", "{ip}", "{version}", {port}, "{username}", "{password}");'
        # print(command)
        cursor.execute(f'{command}')
    except connector.errors.ProgrammingError as e:
        print(e)
    connection.commit()


