from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="16.171.10.180",
        port= 3306,
        #user=input("foo"),
        #password=getpass("Enter password: "),
        user = "foo",
        password = "hejhej",
        database = "Shop"
    ) as connection:
        print(connection)
        query= "SELECT * FROM Products"
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                print(row)
except Error as e:
    print(e)   